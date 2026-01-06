# OpenAI Embedder Configuration (Spock)


This plugin now reads its configuration through the centralized **Spock** system of RAG2F.
The plugin configuration must be placed in the main configuration file (or via environment variables) under the `plugins.<plugin_id>` node.

Note: The APIs in this repository expect the plugin to retrieve the configuration using the `plugin_id` (e.g. `openai_embedder`) via `rag2f.spock.get_plugin_config(plugin_id)`.

## Where to put the configuration

In the main configuration file (e.g. `config.json`), the plugin section should have this structure:

```json
{
  "plugins": {
    "openai_embedder": {
      "api_key": "sk-your-api-key-here",
      "model": "text-embedding-3-small",
      "size": 1536,
      "timeout": 30.0,
      "max_retries": 2
    }
  }
}
```

In this example, the `plugin_id` is `openai_embedder` and Spock will load the configuration when the plugin requests it.

## Environment variables (Spock)

Spock also supports environment variables. The format is based on double underscore prefixes to represent the hierarchy.

Examples to set the plugin configuration via ENV:

```bash
export RAG2F__PLUGINS__OPENAI_EMBEDDER__API_KEY="sk-your-api-key"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__MODEL="text-embedding-3-small"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__SIZE="1536"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__TIMEOUT="30.0"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__MAX_RETRIES="2"
```

Spock applicherà il parsing dei tipi (int, float, bool, JSON) quando possibile.

## Priorità delle sorgenti

1. **Environment Variables** (massima priorità)
2. **File JSON** (config.json passato a RAG2F)
3. **Valori di default nel codice** (minima priorità)

## Esempio: come il plugin accede alla configurazione

Nel codice il plugin ottiene la sua configurazione così:

```python
plugin_cfg = rag2f.spock.get_plugin_config("openai_embedder")
```

Dopo aver ottenuto `plugin_cfg`, il plugin può validare i campi richiesti e lanciare un errore chiaro se mancano.

## Parametri richiesti

- `api_key` (obbligatorio): Chiave API OpenAI
- `model` (obbligatorio): Nome del modello di embedding (es. `"text-embedding-3-small"`, `"text-embedding-3-large"`, `"text-embedding-ada-002"`)
- `size` (obbligatorio): Dimensione del vettore di embedding (1536 per text-embedding-3-small, 3072 per text-embedding-3-large, 1536 per ada-002)
- `timeout` (opzionale): Timeout in secondi (default: 30.0)
- `max_retries` (opzionale): Numero massimo di retry (default: 2)

## Modelli OpenAI disponibili

- `text-embedding-3-small`: 1536 dimensioni (più economico e veloce)
- `text-embedding-3-large`: 3072 dimensioni (migliore qualità)
- `text-embedding-ada-002`: 1536 dimensioni (modello legacy)

## Differenze con Azure OpenAI

A differenza di Azure OpenAI, il plugin OpenAI standard:
- **Non richiede** `azure_endpoint` (usa l'endpoint pubblico OpenAI)
- **Non richiede** `api_version` (usa automaticamente l'ultima versione)
- **Non richiede** `deployment` (usa direttamente il nome del modello)
- Usa il parametro `model` invece di `deployment`
