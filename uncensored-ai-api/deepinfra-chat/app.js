const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const chatOutput = document.getElementById('chat-output');
const loadingIndicator = document.getElementById('loading-indicator');
const modelSelect = document.getElementById('model-select');
const systemPromptInput = document.getElementById('system-prompt-input');

function renderMarkdown(text) {
  if (typeof marked === 'undefined' || typeof DOMPurify === 'undefined') {
    return null;
  }
  marked.setOptions({ breaks: true, gfm: true });
  return DOMPurify.sanitize(marked.parse(text));
}

function appendMessage(text, type) {
  const el = document.createElement('div');
  el.className = `message message--${type}`;

  if (type === 'assistant') {
    const html = renderMarkdown(text);
    if (html) {
      el.classList.add('markdown-body');
      el.innerHTML = html;
    } else {
      el.textContent = text;
    }
  } else {
    el.textContent = text;
  }

  chatOutput.appendChild(el);
  chatOutput.scrollTop = chatOutput.scrollHeight;
}

function setLoading(isLoading) {
  sendButton.disabled = isLoading;
  messageInput.disabled = isLoading;
  modelSelect.disabled = isLoading;
  systemPromptInput.disabled = isLoading;
  loadingIndicator.hidden = !isLoading;
}

async function sendMessage(message) {
  appendMessage(message, 'user');
  setLoading(true);

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        model: modelSelect.value,
        systemPrompt: systemPromptInput.value
      })
    });

    const data = await response.json();

    if (!response.ok) {
      appendMessage(data.error || 'Ein unbekannter Fehler ist aufgetreten.', 'error');
      return;
    }

    appendMessage(data.reply, 'assistant');
  } catch {
    appendMessage('Verbindung zum Server fehlgeschlagen. Läuft der Server?', 'error');
  } finally {
    setLoading(false);
    messageInput.value = '';
    messageInput.focus();
  }
}

chatForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const message = messageInput.value.trim();
  if (!message || sendButton.disabled) return;
  sendMessage(message);
});

messageInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    chatForm.requestSubmit();
  }
});

function showConfigError(message) {
  modelSelect.innerHTML = `<option value="">${message}</option>`;
  systemPromptInput.value = '';
  systemPromptInput.placeholder = message;
}

async function loadConfig() {
  if (window.location.protocol === 'file:') {
    showConfigError('Nicht index.html direkt öffnen — http://localhost:3000');
    return;
  }

  try {
    const response = await fetch('/api/config');
    const data = await response.json();

    if (!response.ok) {
      showConfigError('Konfiguration nicht verfügbar.');
      return;
    }

    if (Array.isArray(data.models) && data.models.length > 0) {
      modelSelect.innerHTML = data.models
        .map(
          (m) =>
            `<option value="${m.id}"${m.id === data.defaultModel ? ' selected' : ''}>${m.label}</option>`
        )
        .join('');
      systemPromptInput.value = data.defaultSystemPrompt || '';
      systemPromptInput.placeholder = 'System-Prompt eingeben …';
      return;
    }

    if (data.model) {
      modelSelect.innerHTML = `<option value="${data.model}" selected>${data.model}</option>`;
      systemPromptInput.value = data.systemPrompt || '';
      systemPromptInput.placeholder = 'System-Prompt eingeben …';
      return;
    }

    showConfigError('Server neu starten: npm start');
  } catch {
    showConfigError('Server nicht erreichbar — npm start, dann http://localhost:3000');
  }
}

loadConfig();
messageInput.focus();
