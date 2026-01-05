# RAG2F OpenAI Embedder Plugin

Plugin per l'integrazione di OpenAI embeddings in RAG2F.

## Struttura del Plugin

```
rag2f_openai_embedder/
├── __init__.py                    # Entry point del plugin
├── plugin.json                    # Metadata del plugin
├── settings.json                  # Settings (vuoto)
├── pyproject.toml                 # Configurazione package Python
├── config.json.example            # Esempio di configurazione
├── CONFIG.md                      # Documentazione configurazione
├── src/
│   ├── __init__.py               # Package src
│   ├── plugin_context.py         # Gestione plugin_id thread-safe
│   ├── embedder.py               # Implementazione OpenAIEmbedder
│   └── bootstrap_hook.py         # Hook di bootstrap
└── test/
    ├── conftest.py               # Configurazione pytest
    ├── test_embedder_unit.py     # Unit test embedder
    └── test_bootstrap_hook.py    # Test bootstrap hook
```

## Parametri di Configurazione

### Obbligatori
- **api_key**: Chiave API OpenAI (es. `"sk-..."`)
- **model**: Nome del modello di embedding
  - `"text-embedding-3-small"` (1536 dim, economico)
  - `"text-embedding-3-large"` (3072 dim, alta qualità)
  - `"text-embedding-ada-002"` (1536 dim, legacy)
- **size**: Dimensione del vettore (1536 o 3072)

### Opzionali
- **timeout**: Timeout richieste in secondi (default: 30.0)
- **max_retries**: Numero massimo di retry (default: 2)

## Differenze rispetto ad Azure OpenAI

Il plugin OpenAI standard differisce da Azure OpenAI per:

1. **NON richiede** `azure_endpoint` (usa endpoint pubblico OpenAI)
2. **NON richiede** `api_version` (usa automaticamente l'ultima versione)
3. **NON richiede** `deployment` (usa direttamente `model`)
4. Utilizza la classe `OpenAI` invece di `AzureOpenAI`

## Configurazione

### Tramite JSON (config.json)

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

### Tramite Variabili d'Ambiente

```bash
export RAG2F__PLUGINS__OPENAI_EMBEDDER__API_KEY="sk-your-api-key"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__MODEL="text-embedding-3-small"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__SIZE="1536"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__TIMEOUT="30.0"
export RAG2F__PLUGINS__OPENAI_EMBEDDER__MAX_RETRIES="2"
```

## Installazione

```bash
cd plugins/rag2f_openai_embedder
pip install -e .
```

## Test

```bash
cd plugins/rag2f_openai_embedder
pytest test/
```

## Utilizzo nel Codice

Il plugin si registra automaticamente tramite il bootstrap hook. Una volta configurato, l'embedder sarà disponibile in RAG2F con l'ID `openai_embedder`.

```python
# Il plugin si carica automaticamente
rag2f = await RAG2F.create(
    plugins_folder="plugins/",
    config=config
)

# L'embedder è disponibile via OptimusPrime
embedder = rag2f.optimus_prime.get("rag2f_openai_embedder")
vector = embedder.getEmbedding("Hello, world!")
```

## Validazione

Il plugin include validazione completa:
- Verifica parametri obbligatori
- Type checking (size, timeout, max_retries)
- Logging dettagliato
- Error handling appropriato

## Test Coverage

- ✅ Validazione configurazione
- ✅ Inizializzazione client
- ✅ Chiamate API corrette
- ✅ Edge cases (stringhe vuote, Unicode)
- ✅ Gestione errori
- ✅ Diversi modelli OpenAI
- ✅ Bootstrap hook

## Release Management

This project uses automated releases with semantic versioning and setuptools-scm.

### Version Schema (PEP 440)

- **Development builds** (branch `dev`): `X.Y.Z.devN` (e.g., `0.1.0.dev123`)
  - Published automatically to TestPyPI on every commit
  - `N` = GitHub Actions run number (monotonically increasing)
  - Base version (`X.Y.Z`) read from `NEXT_VERSION` file

- **Release Candidates** (tags `vX.Y.ZrcN`): `X.Y.ZrcN` (e.g., `1.0.0rc1`)
  - Published to PyPI as pre-release
  - GitHub Release marked as pre-release

- **Stable Releases** (tags `vX.Y.Z`): `X.Y.Z` (e.g., `1.0.0`)
  - Published to PyPI as stable
  - GitHub Release (normal)

### Installing Versions

```bash
# Install latest stable from PyPI
pip install rag2f-openai-embedder

# Install specific stable version
pip install rag2f-openai-embedder==1.0.0

# Install specific release candidate
pip install rag2f-openai-embedder==1.0.0rc1

# Install specific dev build from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            rag2f-openai-embedder==0.1.0.dev123
```

### Version Information at Runtime

Every published package includes commit information:

```python
from rag2f_openai_embedder._version import __version__, __commit__, __distance__

print(f"Version: {__version__}")    # e.g., "1.0.0" or "0.1.0.dev123"
print(f"Commit: {__commit__}")      # Git commit hash
print(f"Distance: {__distance__}")  # Commits since last tag
```

### For Maintainers

#### Publishing Dev Builds
- Push to `dev` branch → automatic publish to TestPyPI
- Version: `<NEXT_VERSION>.dev<run_number>`

#### Creating Releases

**Release Candidate:**
```bash
git tag v1.0.0rc1
git push origin v1.0.0rc1
```

**Stable Release:**
```bash
git tag v1.0.0
git push origin v1.0.0
```

#### Updating Next Version
Edit the `NEXT_VERSION` file and commit to `dev`:
```bash
echo "1.1.0" > NEXT_VERSION
git add NEXT_VERSION
git commit -m "Bump next version to 1.1.0"
git push origin dev
```

### CI/CD Workflows

- **`.github/workflows/ci-dev-testpypi.yml`**: Validates structure, builds, and publishes dev versions to TestPyPI
- **`.github/workflows/release-tags.yml`**: Builds from tags, publishes to PyPI, creates GitHub Releases