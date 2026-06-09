const DEFAULT_JSON = "questions/questions_ai_act_v3_full_default.json";
const DIRECTORY_HANDLE_KEY = "ai-act-tool-directory";

let state = null;
let fileHandle = null;
let directoryHandle = null;
let currentFileName = null;
let saveMode = null;
let hasUnsavedChanges = false;
let activeSectionIndex = 0;
let serverSupportsGenerate = false;

const jsonFileSelect = document.getElementById("jsonFileSelect");
const linkFolderButton = document.getElementById("linkFolderButton");
const saveFileButton = document.getElementById("saveFileButton");
const generateDocumentsButton = document.getElementById("generateDocumentsButton");
const downloadButton = document.getElementById("downloadButton");
const loadExampleButton = document.getElementById("loadExampleButton");
const resetAnswersButton = document.getElementById("resetAnswersButton");
const questionForm = document.getElementById("questionForm");
const sectionNav = document.getElementById("sectionNav");
const saveStatus = document.getElementById("saveStatus");
const progressText = document.getElementById("progressText");

const exampleData = {
  meta: {
    project_name: "AI-Act Dokumentationspaket",
    schema_version: "1.0",
    language: "de",
    updated_at: null
  },
  sections: [
    {
      id: "company",
      title: "Unternehmen",
      description: "Basisdaten des Unternehmens und der verantwortlichen Person.",
      questions: [
        {
          id: "company_name",
          label: "Name des Unternehmens",
          type: "text",
          required: true,
          answer: ""
        },
        {
          id: "industry",
          label: "Branche",
          type: "select",
          required: true,
          options: [
            "Versicherung",
            "Finanzdienstleistung",
            "Gesundheit",
            "Bildung",
            "Industrie",
            "Handel",
            "IT / Software",
            "Sonstiges"
          ],
          answer: ""
        },
        {
          id: "contact_person",
          label: "Verantwortliche Person",
          type: "text",
          required: false,
          answer: ""
        }
      ]
    },
    {
      id: "ai_system",
      title: "KI-System",
      description: "Beschreibung des KI-Systems, seines Zwecks und seiner Nutzergruppen.",
      questions: [
        {
          id: "ai_system_name",
          label: "Name des KI-Systems",
          type: "text",
          required: true,
          answer: ""
        },
        {
          id: "purpose",
          label: "Was soll das KI-System tun?",
          type: "textarea",
          required: true,
          help: "Beschreiben Sie den konkreten Zweck möglichst verständlich.",
          answer: ""
        },
        {
          id: "deployment_status",
          label: "Status",
          type: "radio",
          required: true,
          options: ["Idee", "Prototyp", "Pilot", "Produktiv", "Eingestellt"],
          answer: ""
        },
        {
          id: "user_groups",
          label: "Wer nutzt das System?",
          type: "checkbox",
          required: false,
          options: [
            "Mitarbeitende",
            "Führungskräfte",
            "Kunden",
            "Makler / Vertriebspartner",
            "Endverbraucher",
            "Externe Dienstleister"
          ],
          answer: []
        }
      ]
    },
    {
      id: "ai_act",
      title: "AI-Act Ersteinschätzung",
      description: "Fragen zur vorläufigen Risikoklassifizierung.",
      questions: [
        {
          id: "external_ai_service",
          label: "Wird ein externer KI-Dienst genutzt?",
          type: "radio",
          required: true,
          options: ["Ja", "Nein", "Unklar"],
          answer: ""
        },
        {
          id: "role",
          label: "Welche Rolle trifft am ehesten zu?",
          type: "select",
          required: true,
          options: [
            "Betreiber / Deployer",
            "Anbieter / Provider",
            "Importeur",
            "Händler / Distributor",
            "Produkthersteller",
            "Unklar"
          ],
          answer: ""
        },
        {
          id: "sensitive_contexts",
          label: "In welchen sensiblen Bereichen wird das System eingesetzt?",
          type: "checkbox",
          required: false,
          options: [
            "Recruiting / Bewerberauswahl",
            "Beschäftigtenbewertung",
            "Kreditwürdigkeitsprüfung",
            "Versicherung / Risikobewertung natürlicher Personen",
            "Bildung / Prüfung / Bewertung",
            "Kritische Infrastruktur",
            "Gesundheit / Medizin",
            "Biometrie",
            "Zugang zu wesentlichen Dienstleistungen",
            "Keiner dieser Bereiche"
          ],
          answer: []
        },
        {
          id: "human_oversight",
          label: "Gibt es eine menschliche Kontrolle der KI-Ergebnisse?",
          type: "radio",
          required: true,
          options: [
            "Ja, finale Entscheidung durch Menschen",
            "Teilweise",
            "Nein, vollautomatisch",
            "Unklar"
          ],
          answer: ""
        },
        {
          id: "personal_data",
          label: "Werden personenbezogene Daten verarbeitet?",
          type: "radio",
          required: true,
          options: ["Ja", "Nein", "Unklar"],
          answer: ""
        },
        {
          id: "notes",
          label: "Offene Punkte / Hinweise",
          type: "textarea",
          required: false,
          answer: ""
        }
      ]
    }
  ]
};

jsonFileSelect.addEventListener("change", () => {
  const filename = jsonFileSelect.value;
  if (!filename || filename === currentFileName) return;
  if (hasUnsavedChanges && !confirm("Ungespeicherte Änderungen verwerfen und andere Datei laden?")) {
    jsonFileSelect.value = currentFileName || "";
    return;
  }
  loadJsonFile(filename);
});

linkFolderButton.addEventListener("click", linkLocalFolder);
saveFileButton.addEventListener("click", saveToOriginalFile);
generateDocumentsButton.addEventListener("click", generateDocuments);
downloadButton.addEventListener("click", () => downloadJson());
loadExampleButton.addEventListener("click", () => loadData(structuredClone(exampleData), null, "example"));
resetAnswersButton.addEventListener("click", resetAnswers);

document.addEventListener("DOMContentLoaded", init);

window.addEventListener("beforeunload", (event) => {
  if (!hasUnsavedChanges) return;
  event.preventDefault();
  event.returnValue = "";
});

async function init() {
  if (window.showDirectoryPicker) {
    linkFolderButton.hidden = false;
  }

  const urlFile = new URLSearchParams(window.location.search).get("file");
  const preferredFile = urlFile || DEFAULT_JSON;

  if (await tryLoadViaHttp(preferredFile)) {
    await refreshJsonFileList();
    await checkServerCapabilities();
    return;
  }

  if (await tryLoadViaDirectoryHandle(preferredFile)) {
    await refreshJsonFileList();
    return;
  }

  jsonFileSelect.innerHTML = `<option value="">Keine Datei geladen</option>`;
}

async function tryLoadViaHttp(filename) {
  try {
    const response = await fetch(filename, { cache: "no-store" });
    if (!response.ok) return false;

    const json = await response.json();
    loadData(json, filename, "http");
    return true;
  } catch {
    return false;
  }
}

async function tryLoadViaDirectoryHandle(filename) {
  const storedHandle = await getStoredDirectoryHandle();
  if (!storedHandle) return false;

  try {
    const permission = await storedHandle.queryPermission({ mode: "readwrite" });
    if (permission !== "granted") {
      const requested = await storedHandle.requestPermission({ mode: "readwrite" });
      if (requested !== "granted") return false;
    }

    directoryHandle = storedHandle;
    await loadJsonFromDirectory(filename);
    return true;
  } catch {
    return false;
  }
}

async function linkLocalFolder() {
  if (!window.showDirectoryPicker) {
    alert("Ihr Browser unterstützt das Verknüpfen eines Ordners nicht. Bitte python server.py nutzen.");
    return;
  }

  try {
    directoryHandle = await window.showDirectoryPicker({ mode: "readwrite" });
    await storeDirectoryHandle(directoryHandle);
    await refreshJsonFileList();
    await loadJsonFromDirectory(jsonFileSelect.value || DEFAULT_JSON);
  } catch (error) {
    if (error.name !== "AbortError") {
      alert("Ordner konnte nicht verknüpft werden: " + error.message);
    }
  }
}

async function refreshJsonFileList() {
  const files = await listJsonFiles();
  const previous = currentFileName;

  jsonFileSelect.innerHTML = files
    .map((file) => {
      const label = file.includes("/") ? file.split("/").pop() : file;
      return `<option value="${escapeHtml(file)}">${escapeHtml(label)}</option>`;
    })
    .join("");

  jsonFileSelect.disabled = files.length === 0;

  if (files.length === 0) {
    jsonFileSelect.innerHTML = `<option value="">Keine JSON-Dateien gefunden</option>`;
    return;
  }

  if (previous && files.includes(previous)) {
    jsonFileSelect.value = previous;
  } else if (files.includes(DEFAULT_JSON)) {
    jsonFileSelect.value = DEFAULT_JSON;
  } else {
    jsonFileSelect.value = files[0];
  }
}

async function listJsonFiles() {
  if (saveMode === "http") {
    try {
      const response = await fetch("/api/json/list", { cache: "no-store" });
      if (response.ok) {
        const files = await response.json();
        return Array.isArray(files) ? files : [];
      }
    } catch {
      // Fallback below.
    }
  }

  if (directoryHandle) {
    try {
      const questionsDir = await directoryHandle.getDirectoryHandle("questions");
      const files = [];
      for await (const entry of questionsDir.values()) {
        if (entry.kind === "file" && entry.name.endsWith(".json")) {
          files.push(`questions/${entry.name}`);
        }
      }
      return files.sort();
    } catch {
      // Fallback below.
    }
  }

  if (currentFileName) {
    return [currentFileName];
  }

  return [];
}

async function loadJsonFile(filename) {
  if (!filename) return;

  if (saveMode === "http") {
    if (await tryLoadViaHttp(filename)) {
      jsonFileSelect.value = filename;
    }
    return;
  }

  if (directoryHandle) {
    await loadJsonFromDirectory(filename);
    jsonFileSelect.value = filename;
    return;
  }

  if (await tryLoadViaHttp(filename)) {
    await refreshJsonFileList();
    jsonFileSelect.value = filename;
    return;
  }

  alert("Datei kann nicht geladen werden. Bitte python server.py starten oder den Ordner verknüpfen.");
}

async function loadJsonFromDirectory(filename) {
  if (!directoryHandle) {
    throw new Error("Kein Ordner verknüpft.");
  }

  const parts = filename.split("/");
  let dir = directoryHandle;

  for (let index = 0; index < parts.length - 1; index += 1) {
    dir = await dir.getDirectoryHandle(parts[index]);
  }

  fileHandle = await dir.getFileHandle(parts[parts.length - 1]);
  const file = await fileHandle.getFile();
  const json = JSON.parse(await file.text());

  loadData(json, filename, "fsa");
}

function loadData(json, filename = null, mode = null) {
  validateData(json);
  state = json;
  hasUnsavedChanges = false;
  activeSectionIndex = 0;

  if (filename) currentFileName = filename;
  if (mode) saveMode = mode;

  questionForm.hidden = false;
  saveFileButton.disabled = saveMode === "example";
  updateGenerateButtonState();
  downloadButton.disabled = false;
  resetAnswersButton.disabled = false;

  if (currentFileName && jsonFileSelect.options.length) {
    jsonFileSelect.value = currentFileName;
  }

  renderNavigation();
  renderForm();
  updateProgress();

  if (saveMode === "http" || saveMode === "fsa") {
    setStatus(`${displayFileName(currentFileName)} geladen`, "saved");
  } else if (saveMode === "example") {
    setStatus("Beispiel geladen (nicht gespeichert)", "saved");
  }
}

function displayFileName(filename) {
  if (!filename) return "";
  return filename.includes("/") ? filename.split("/").pop() : filename;
}

function isQuestionAnswered(question) {
  if (Array.isArray(question.answer)) return question.answer.length > 0;
  return String(question.answer ?? "").trim() !== "";
}

function isSectionComplete(section) {
  return section.questions.length > 0 && section.questions.every(isQuestionAnswered);
}

function validateData(json) {
  if (!json || !Array.isArray(json.sections)) {
    throw new Error("Ungültiges Format. Erwartet wird ein Objekt mit einer sections-Liste.");
  }

  for (const section of json.sections) {
    if (!section.id || !section.title || !Array.isArray(section.questions)) {
      throw new Error("Jeder Abschnitt benötigt id, title und questions.");
    }

    for (const question of section.questions) {
      if (!question.id || !question.label || !question.type) {
        throw new Error("Jede Frage benötigt id, label und type.");
      }
    }
  }
}

function renderNavigation() {
  sectionNav.innerHTML = "";

  state.sections.forEach((section, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "nav-item";
    button.textContent = section.title;
    button.title = section.title;

    if (index === activeSectionIndex) {
      button.classList.add("active");
    }
    if (isSectionComplete(section)) {
      button.classList.add("answered");
    }

    button.addEventListener("click", () => {
      activeSectionIndex = index;
      updateNavigationActive();
      renderForm();
    });

    sectionNav.appendChild(button);
  });
}

function updateNavigationActive() {
  const buttons = sectionNav.querySelectorAll(".nav-item");
  buttons.forEach((button, index) => {
    button.classList.toggle("active", index === activeSectionIndex);
  });
}

function updateNavigationProgress() {
  const buttons = sectionNav.querySelectorAll(".nav-item");
  state.sections.forEach((section, index) => {
    const button = buttons[index];
    if (!button) return;
    button.classList.toggle("answered", isSectionComplete(section));
  });
}

function renderForm() {
  questionForm.innerHTML = "";

  const section = state.sections[activeSectionIndex];
  if (!section) return;

  const sectionEl = document.createElement("section");
  sectionEl.className = "section";
  sectionEl.id = "section-" + section.id;

  const header = document.createElement("div");
  header.className = "section-header";
  header.innerHTML = `
    <h2 class="section-title">${escapeHtml(section.title)}</h2>
    ${section.description ? `<p class="section-description">${escapeHtml(section.description)}</p>` : ""}
  `;
  sectionEl.appendChild(header);

  section.questions.forEach((question) => {
    const questionEl = createQuestionElement(section.id, question);
    sectionEl.appendChild(questionEl);
  });

  questionForm.appendChild(sectionEl);
}

function createQuestionElement(sectionId, question) {
  const wrapper = document.createElement("div");
  wrapper.className = "question";

  const fieldName = `${sectionId}.${question.id}`;
  const requiredMark = question.required ? '<span class="required"> *</span>' : "";
  const help = question.help ? `<p class="help">${escapeHtml(question.help)}</p>` : "";
  const meta = `<div class="meta">ID: ${escapeHtml(question.id)} | Typ: ${escapeHtml(question.type)}</div>`;

  if (["text", "date", "number"].includes(question.type)) {
    wrapper.innerHTML = `
      <label for="${fieldName}">${escapeHtml(question.label)}${requiredMark}</label>
      ${help}
      <input id="${fieldName}" name="${fieldName}" type="${question.type}" value="${escapeHtml(question.answer ?? "")}" ${question.required ? "required" : ""} />
      ${meta}
    `;

    wrapper.querySelector("input").addEventListener("input", (event) => {
      question.answer = event.target.value;
      markUnsaved();
    });
  }

  if (question.type === "textarea") {
    wrapper.innerHTML = `
      <label for="${fieldName}">${escapeHtml(question.label)}${requiredMark}</label>
      ${help}
      <textarea id="${fieldName}" name="${fieldName}" ${question.required ? "required" : ""}>${escapeHtml(question.answer ?? "")}</textarea>
      ${meta}
    `;

    wrapper.querySelector("textarea").addEventListener("input", (event) => {
      question.answer = event.target.value;
      markUnsaved();
    });
  }

  if (question.type === "select") {
    const options = (question.options || [])
      .map((option) => `<option value="${escapeHtml(option)}" ${option === question.answer ? "selected" : ""}>${escapeHtml(option)}</option>`)
      .join("");

    wrapper.innerHTML = `
      <label for="${fieldName}">${escapeHtml(question.label)}${requiredMark}</label>
      ${help}
      <select id="${fieldName}" name="${fieldName}" ${question.required ? "required" : ""}>
        <option value="">Bitte auswählen</option>
        ${options}
      </select>
      ${meta}
    `;

    wrapper.querySelector("select").addEventListener("change", (event) => {
      question.answer = event.target.value;
      markUnsaved();
    });
  }

  if (question.type === "radio") {
    const options = (question.options || [])
      .map((option, index) => {
        const optionId = `${fieldName}.${index}`;
        return `
          <label class="option" for="${optionId}">
            <input id="${optionId}" type="radio" name="${fieldName}" value="${escapeHtml(option)}" ${option === question.answer ? "checked" : ""} />
            <span>${escapeHtml(option)}</span>
          </label>
        `;
      })
      .join("");

    wrapper.innerHTML = `
      <fieldset>
        <legend>${escapeHtml(question.label)}${requiredMark}</legend>
        ${help}
        <div class="option-list">${options}</div>
      </fieldset>
      ${meta}
    `;

    wrapper.querySelectorAll("input[type='radio']").forEach((input) => {
      input.addEventListener("change", (event) => {
        question.answer = event.target.value;
        markUnsaved();
      });
    });
  }

  if (question.type === "checkbox") {
    if (!Array.isArray(question.answer)) question.answer = [];

    const options = (question.options || [])
      .map((option, index) => {
        const optionId = `${fieldName}.${index}`;
        const checked = question.answer.includes(option);
        return `
          <label class="option" for="${optionId}">
            <input id="${optionId}" type="checkbox" name="${fieldName}" value="${escapeHtml(option)}" ${checked ? "checked" : ""} />
            <span>${escapeHtml(option)}</span>
          </label>
        `;
      })
      .join("");

    wrapper.innerHTML = `
      <fieldset>
        <legend>${escapeHtml(question.label)}${requiredMark}</legend>
        ${help}
        <div class="option-list">${options}</div>
      </fieldset>
      ${meta}
    `;

    wrapper.querySelectorAll("input[type='checkbox']").forEach((input) => {
      input.addEventListener("change", () => {
        question.answer = Array.from(wrapper.querySelectorAll("input[type='checkbox']:checked")).map((item) => item.value);
        markUnsaved();
      });
    });
  }

  return wrapper;
}

function markUnsaved() {
  hasUnsavedChanges = true;
  if (state?.meta) {
    state.meta.updated_at = new Date().toISOString();
  }
  setStatus("Ungespeicherte Änderungen", "unsaved");
  updateProgress();
  updateNavigationProgress();
}

function updateProgress() {
  if (!state) {
    progressText.textContent = "0 / 0 beantwortet";
    return;
  }

  const questions = state.sections.flatMap((section) => section.questions);
  const answered = questions.filter(isQuestionAnswered).length;

  progressText.textContent = `${answered} / ${questions.length} beantwortet`;
}

async function saveToOriginalFile() {
  if (!state) return;

  if (saveMode === "http" && currentFileName) {
    try {
      const response = await fetch(`/api/json?file=${encodeURIComponent(currentFileName)}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(state, null, 2)
      });

      if (response.ok) {
        hasUnsavedChanges = false;
        setStatus(`${currentFileName} gespeichert`, "saved");
        return;
      }
    } catch {
      // Fallback below.
    }
  }

  if (saveMode === "fsa" && fileHandle) {
    try {
      const writable = await fileHandle.createWritable();
      await writable.write(JSON.stringify(state, null, 2));
      await writable.close();

      hasUnsavedChanges = false;
      setStatus(`${currentFileName} gespeichert`, "saved");
      return;
    } catch (error) {
      alert("Die Datei konnte nicht gespeichert werden: " + error.message);
      return;
    }
  }

  downloadJson(currentFileName || undefined);
}

async function checkServerCapabilities() {
  try {
    const response = await fetch("/api/health", { cache: "no-store" });
    const data = await parseJsonResponse(response);
    serverSupportsGenerate = data.generate === true;
  } catch {
    serverSupportsGenerate = false;
  }

  updateGenerateButtonState();
}

function updateGenerateButtonState() {
  generateDocumentsButton.disabled = saveMode !== "http" || !serverSupportsGenerate;
  generateDocumentsButton.title =
    saveMode === "http" && !serverSupportsGenerate
      ? "Alten Server beenden und py -3 server.py neu starten"
      : "";
}

async function parseJsonResponse(response) {
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    throw new Error(
      "Der Server antwortet nicht mit JSON. Bitte alle laufenden Server auf Port 8080 beenden und dann py -3 server.py neu starten."
    );
  }
  return response.json();
}

async function generateDocuments() {
  if (!state) return;

  if (saveMode !== "http") {
    alert("Word-Dokumente können nur über den lokalen Server erzeugt werden. Bitte py -3 server.py starten.");
    return;
  }

  if (!serverSupportsGenerate) {
    alert(
      "Dokumentenerstellung nicht verfügbar. Bitte alle alten Server-Prozesse beenden und den Server neu starten:\n\npy -3 server.py"
    );
    return;
  }

  if (!currentFileName) {
    alert("Keine JSON-Datei geladen.");
    return;
  }

  if (hasUnsavedChanges) {
    await saveToOriginalFile();
  }

  generateDocumentsButton.disabled = true;
  setStatus("Dokumente werden erstellt …", "unsaved");

  try {
    const response = await fetch(`/api/generate?file=${encodeURIComponent(currentFileName)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(state, null, 2)
    });

    const result = await parseJsonResponse(response);
    if (!response.ok || !result.ok) {
      throw new Error(result.error || "Dokumente konnten nicht erstellt werden.");
    }

    hasUnsavedChanges = false;
    setStatus(`${result.count} Word-Dokumente erstellt`, "saved");

    if (result.zip) {
      window.location.href = result.zip;
    }
  } catch (error) {
    alert("Fehler bei der Dokumentenerstellung: " + error.message);
    setStatus("Dokumentenerstellung fehlgeschlagen", "unsaved");
  } finally {
    updateGenerateButtonState();
  }
}

async function downloadJson(filename = createDownloadFilename()) {
  if (!state) return;

  const content = JSON.stringify(state, null, 2);
  const blob = new Blob([content], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();

  URL.revokeObjectURL(url);

  if (saveMode !== "example") {
    hasUnsavedChanges = false;
    setStatus(`${filename} heruntergeladen`, "saved");
  }
}

function createDownloadFilename() {
  if (currentFileName && currentFileName.endsWith(".json")) {
    return currentFileName;
  }

  const project = state?.meta?.project_name || "ai-act-dokumentation";
  const safeProject = project
    .toLowerCase()
    .replaceAll("ä", "ae")
    .replaceAll("ö", "oe")
    .replaceAll("ü", "ue")
    .replaceAll("ß", "ss")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");

  const date = new Date().toISOString().slice(0, 10);
  return `${safeProject}-${date}.json`;
}

async function getStoredDirectoryHandle() {
  if (!("indexedDB" in window)) return null;

  const db = await openHandleDatabase();
  const handle = await readDirectoryHandle(db);
  db.close();
  return handle;
}

async function storeDirectoryHandle(handle) {
  if (!("indexedDB" in window)) return;

  const db = await openHandleDatabase();
  await writeDirectoryHandle(db, handle);
  db.close();
}

function openHandleDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("ai-act-web-tool", 1);

    request.onupgradeneeded = () => {
      request.result.createObjectStore("handles");
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

function readDirectoryHandle(db) {
  return new Promise((resolve, reject) => {
    const transaction = db.transaction("handles", "readonly");
    const store = transaction.objectStore("handles");
    const request = store.get(DIRECTORY_HANDLE_KEY);

    request.onsuccess = () => resolve(request.result || null);
    request.onerror = () => reject(request.error);
  });
}

function writeDirectoryHandle(db, handle) {
  return new Promise((resolve, reject) => {
    const transaction = db.transaction("handles", "readwrite");
    const store = transaction.objectStore("handles");
    const request = store.put(handle, DIRECTORY_HANDLE_KEY);

    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
}

function resetAnswers() {
  if (!state) return;

  const confirmed = confirm("Sollen wirklich alle Antworten geleert werden?");
  if (!confirmed) return;

  state.sections.forEach((section) => {
    section.questions.forEach((question) => {
      question.answer = question.type === "checkbox" ? [] : "";
    });
  });

  markUnsaved();
  renderForm();
  updateNavigationProgress();
}

function setStatus(text, type) {
  saveStatus.textContent = text;
  saveStatus.className = "status " + type;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
