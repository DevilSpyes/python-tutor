# Changelog - Netlify Static Conversion

## [1.0.0] - 2025-11-23

### Added
- **REMOVE_MODELS.md**: Instructions for handling large model files.
- **README_NETLIFY.md**: Comprehensive deployment guide.
- **CHECKLIST_DEPLOYMENT.md**: Verification steps.
- **static/test_chat_connection.js**: Utility to verify API connections.

### Changed
- **AI Panel UI**: Refactored to support "API Key" vs "Remote Model" modes with explicit configuration.
- **AI Logic**: Removed all server-side proxying. Chat requests now go directly from browser to provider (OpenAI/Groq/Custom).
- **Backend**: Disabled server-side execution in `main.py` via `ALLOW_SERVER_EXECUTION` flag.
- **Project Structure**: Cleaned up `.gguf` and large binaries.

### Removed
- Legacy server-side chat endpoints.
- Large model binaries from repository.
