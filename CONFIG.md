# OpenAI Embedder Configuration (Spock)

This plugin now reads configuration through RAG2F's centralized **Spock** system.
The plugin configuration must be placed in the main configuration file (or via environment variables) under the `plugins.<plugin_id>` node.

Note: the APIs in this repository expect the plugin to fetch configuration using the `plugin_id` (e.g. `openai_embedder`) via `rag2f.spock.get_plugin_config(plugin_id)`.

## Where to Put the Configuration

In the main configuration file (e.g. `config.json`) the plugin section should have this structure:

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

In this example the `plugin_id` is `openai_embedder` and Spock will load the configuration when the plugin requests it.

## Environment Variables (Spock)

Spock also supports environment variables. The format is based on prefixes with double underscores to represent the hierarchy.

Examples for setting plugin configuration via ENV:

```bash
export RAG2F__PLUGINS__OPENAI_EMBEDDER__API_KEY="sk-your-api-key"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__MODEL="text-embedding-3-small"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__SIZE="1536"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__TIMEOUT="30.0"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__MAX_RETRIES="2"
```

Spock will parse types (int, float, bool, JSON) when possible.

## Source Priority

1. **Environment Variables** (highest priority)
2. **JSON File** (`config.json` passed to RAG2F)
3. **Default values in code** (lowest priority)

## Example: How the Plugin Accesses Configuration

In code the plugin retrieves its configuration like this:

```python
plugin_cfg = rag2f.spock.get_plugin_config("openai_embedder")
```

After obtaining `plugin_cfg`, the plugin can validate required fields and raise a clear error if they are missing.

## Required Parameters

- `api_key` (required): OpenAI API key
- `model` (required): Embedding model name (e.g. `"text-embedding-3-small"`, `"text-embedding-3-large"`, `"text-embedding-ada-002"`)
- `size` (required): Embedding vector dimension (1536 for text-embedding-3-small, 3072 for text-embedding-3-large, 1536 for ada-002)
- `timeout` (optional): Timeout in seconds (default: 30.0)
- `max_retries` (optional): Maximum number of retries (default: 2)

## Available OpenAI Models

- `text-embedding-3-small`: 1536 dimensions (more economical and faster)
- `text-embedding-3-large`: 3072 dimensions (better quality)
- `text-embedding-ada-002`: 1536 dimensions (legacy model)

## Differences from Azure OpenAI

Unlike Azure OpenAI, the standard OpenAI plugin:
- **Does not require** `azure_endpoint` (uses the OpenAI public endpoint)
- **Does not require** `api_version` (automatically uses the latest version)
- **Does not require** `deployment` (directly uses the model name)
- Uses the `model` parameter instead of `deployment`
