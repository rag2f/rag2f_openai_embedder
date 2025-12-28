# RAG2F OpenAI Embedder Plugin

Plugin for integrating OpenAI embeddings into RAG2F.

## Plugin Structure

```
rag2f_openai_embedder/
├── __init__.py                    # Plugin entry point
├── plugin.json                    # Plugin metadata
├── settings.json                  # Settings (empty)
├── pyproject.toml                 # Python package configuration
├── config.json.example            # Configuration example
├── CONFIG.md                      # Configuration documentation
├── src/
│   ├── __init__.py               # src package
│   ├── plugin_context.py         # Thread-safe plugin_id management
│   ├── embedder.py               # OpenAIEmbedder implementation
│   └── bootstrap_hook.py         # Bootstrap hook
└── test/
    ├── conftest.py               # Pytest configuration
    ├── test_embedder_unit.py     # Embedder unit tests
    └── test_bootstrap_hook.py    # Bootstrap hook tests
```

## Configuration Parameters

### Required
- **api_key**: OpenAI API key (e.g. `"sk-..."`)
- **model**: Embedding model name
  - `"text-embedding-3-small"` (1536 dim, cost-effective)
  - `"text-embedding-3-large"` (3072 dim, higher quality)
  - `"text-embedding-ada-002"` (1536 dim, legacy)
- **size**: Vector dimension (1536 or 3072)

### Optional
- **timeout**: Request timeout in seconds (default: 30.0)
- **max_retries**: Maximum number of retries (default: 2)

## Differences vs Azure OpenAI

The standard OpenAI plugin differs from Azure OpenAI because:

1. **Does NOT require** `azure_endpoint` (uses OpenAI public endpoint)
2. **Does NOT require** `api_version` (automatically uses the latest version)
3. **Does NOT require** `deployment` (directly uses `model`)
4. Uses the `OpenAI` class instead of `AzureOpenAI`

## Configuration

### Via JSON (config.json)

```json
{
  "plugins": {
    "openai_embedder": {
      "api_key": "sk-your-api-key",
      "model": "text-embedding-3-small",
      "size": 1536,
      "timeout": 30.0,
      "max_retries": 2
    }
  }
}
```

### Via Environment Variables

```bash
export RAG2F__PLUGINS__OPENAI_EMBEDDER__API_KEY="sk-your-api-key"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__MODEL="text-embedding-3-small"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__SIZE="1536"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__TIMEOUT="30.0"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__MAX_RETRIES="2"
```

## Installation

```bash
cd plugins/rag2f_openai_embedder
pip install -e .
```

## Tests

```bash
cd plugins/rag2f_openai_embedder
pytest test/
```

## Usage in Code

The plugin registers automatically through the bootstrap hook. Once configured, the embedder will be available in RAG2F with the ID `openai_embedder`.

```python
# The plugin loads automatically
rag2f = await RAG2F.create(
    plugins_folder="plugins/",
    config=config
)

# The embedder is available via OptimusPrime
embedder = rag2f.optimus_prime.get("rag2f_openai_embedder")
vector = embedder.getEmbedding("Hello, world!")
```

## Validation

The plugin includes full validation:
- Checks required parameters
- Type checking (size, timeout, max_retries)
- Detailed logging
- Appropriate error handling

## Test Coverage

- ✅ Configuration validation
- ✅ Client initialization
- ✅ Correct API calls
- ✅ Edge cases (empty strings, Unicode)
- ✅ Error handling
- ✅ Different OpenAI models
- ✅ Bootstrap hook
