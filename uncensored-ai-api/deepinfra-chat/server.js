require('dotenv').config();

const express = require('express');
const path = require('path');
const config = require('./config');

const app = express();
const PORT = process.env.PORT || 3000;
const allowedModels = new Set(config.deepinfra.models.map((m) => m.id));

app.use(express.json());

function getApiKey() {
  return process.env.DEEP_INFRA_API_KEY || process.env.DEEPINFRA_API_KEY;
}

function resolveModel(model) {
  if (typeof model === 'string' && allowedModels.has(model)) {
    return model;
  }
  return config.deepinfra.defaultModel;
}

function resolveSystemPrompt(systemPrompt) {
  if (typeof systemPrompt === 'string' && systemPrompt.trim()) {
    return systemPrompt.trim();
  }
  return config.deepinfra.defaultSystemPrompt;
}

app.get('/api/config', (_req, res) => {
  res.json({
    defaultModel: config.deepinfra.defaultModel,
    defaultSystemPrompt: config.deepinfra.defaultSystemPrompt,
    models: config.deepinfra.models
  });
});

app.post('/api/chat', async (req, res) => {
  const { message, model, systemPrompt } = req.body;

  if (!message || typeof message !== 'string' || !message.trim()) {
    return res.status(400).json({ error: 'Bitte gib eine Nachricht ein.' });
  }

  const apiKey = getApiKey();
  if (!apiKey) {
    return res.status(500).json({
      error:
        'Kein API-Key gefunden. Bitte DEEP_INFRA_API_KEY oder DEEPINFRA_API_KEY in der .env-Datei setzen.'
    });
  }

  const selectedModel = resolveModel(model);
  const selectedSystemPrompt = resolveSystemPrompt(systemPrompt);

  try {
    const response = await fetch(config.deepinfra.apiUrl, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: selectedModel,
        messages: [
          {
            role: 'system',
            content: selectedSystemPrompt
          },
          {
            role: 'user',
            content: message.trim()
          }
        ],
        temperature: config.deepinfra.temperature,
        max_tokens: config.deepinfra.maxTokens
      })
    });

    const data = await response.json();

    if (!response.ok) {
      const errorMessage =
        data?.error?.message ||
        data?.message ||
        `DeepInfra-Anfrage fehlgeschlagen (Status ${response.status}).`;
      return res.status(response.status).json({ error: errorMessage });
    }

    const reply = data?.choices?.[0]?.message?.content;
    if (!reply) {
      return res.status(502).json({
        error: 'Keine Antwort von der KI erhalten. Bitte versuche es erneut.'
      });
    }

    return res.json({ reply });
  } catch (err) {
    console.error('Chat-Fehler:', err);
    return res.status(500).json({
      error: 'Verbindung zu DeepInfra fehlgeschlagen. Bitte später erneut versuchen.'
    });
  }
});

app.use(express.static(path.join(__dirname)));

app.listen(PORT, () => {
  console.log(`DeepInfra Chat läuft unter http://localhost:${PORT}`);
});
