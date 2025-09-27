# Open WebUI Project Dependencies

## Project Overview
- **Project Name**: open-webui
- **Version**: 0.6.31
- **Description**: Open WebUI - A comprehensive web-based AI chat interface
- **License**: Other/Proprietary License
- **Repository Type**: Full-stack application with Python backend and Svelte frontend

## Runtime Environment Versions

### System Requirements
- **Python Version**: 3.12.8 (as specified in `.python-version`)
- **Python Range**: >= 3.11, < 3.13.0a1 (as specified in `pyproject.toml`)
- **Node.js Version**: Currently installed v23.7.0 (Project requires: >=18.13.0 <=22.x.x)
- **npm Version**: Currently installed 11.5.2 (Project requires: >=6.0.0)
- **UV Package Manager**: 0.6.14 (a4cec56dc 2025-04-09)

### Local Development Environment
- **Direct Installation**: No containerization required
- **CUDA Support**: Available through direct PyTorch installation if needed
- **Ollama Support**: Can be installed locally if required

## Frontend Dependencies

### Core Framework & Build Tools
- **Svelte**: ^4.2.18
- **SvelteKit**: ^2.5.20
- **Vite**: ^5.4.14
- **TypeScript**: ^5.5.4
- **Adapter**: @sveltejs/adapter-static ^3.0.2, @sveltejs/adapter-node ^2.0.0

### UI & Styling
- **TailwindCSS**: ^4.0.0
- **@tailwindcss/typography**: ^0.5.13
- **@tailwindcss/container-queries**: ^0.1.1
- **@tailwindcss/postcss**: ^4.0.0
- **PostCSS**: ^8.4.31
- **Sass**: sass-embedded ^1.81.0

### Rich Text Editor
- **TipTap Core**: ^3.0.7
- **TipTap Extensions**: Multiple extensions (^2.26.1 to ^3.4.5)
- **ProseMirror**: Multiple packages (^1.2.2 to ^1.34.3)
- **CodeMirror**: ^6.0.1 with language support

### Data Visualization & Charts
- **Chart.js**: ^4.5.0
- **Mermaid**: ^11.10.1
- **@xyflow/svelte**: ^0.1.19
- **Leaflet**: ^1.9.4

### File Processing & Utilities
- **PDF.js**: ^5.4.149
- **jsPDF**: ^3.0.0
- **html2canvas-pro**: ^1.5.11
- **file-saver**: ^2.0.5
- **DOMPurify**: ^3.2.6
- **Marked**: ^9.1.0
- **Turndown**: ^7.2.0
- **KaTeX**: ^0.16.22

### AI & ML Libraries
- **@huggingface/transformers**: ^3.0.0
- **@mediapipe/tasks-vision**: ^0.10.17
- **Pyodide**: ^0.28.2
- **@pyscript/core**: ^0.4.32

### Authentication & Security
- **@azure/msal-browser**: ^4.5.0

### Internationalization
- **i18next**: ^23.10.0
- **i18next-browser-languagedetector**: ^7.2.0
- **i18next-resources-to-backend**: ^1.2.0

### Development Dependencies
- **ESLint**: ^8.56.0
- **Prettier**: ^3.3.3
- **Cypress**: ^13.15.0
- **Vitest**: ^1.6.1
- **svelte-check**: ^3.8.5

## Backend Dependencies

### Core Framework
- **FastAPI**: 0.115.7
- **Uvicorn**: 0.35.0 (with standard extras)
- **Pydantic**: 2.11.7
- **Starlette**: starlette-compress 1.6.0

### Authentication & Security
- **python-jose**: 3.4.0
- **PyJWT**: 2.10.1 (with crypto extras)
- **passlib**: 1.7.4 (with bcrypt extras)
- **bcrypt**: 4.3.0
- **argon2-cffi**: 25.1.0
- **cryptography**: Latest
- **authlib**: 1.6.3

### Database & ORM
- **SQLAlchemy**: 2.0.38
- **Alembic**: 1.14.0
- **Peewee**: 3.18.1
- **peewee-migrate**: 1.12.2
- **PyMySQL**: 1.1.1
- **psycopg2-binary**: 2.9.10 (PostgreSQL)
- **pgvector**: 0.4.1
- **pymongo**: Latest (MongoDB)
- **oracledb**: 3.2.0

### HTTP & Networking
- **requests**: 2.32.5
- **aiohttp**: 3.12.15
- **httpx**: 0.28.1 (with multiple extras)
- **async-timeout**: Latest
- **aiofiles**: Latest

### AI & ML Libraries
- **OpenAI**: Latest
- **Anthropic**: Latest
- **google-genai**: 1.38.0
- **google-generativeai**: 0.8.5
- **langchain**: 0.3.27
- **langchain-community**: 0.3.29
- **transformers**: Latest
- **sentence-transformers**: 5.1.1
- **accelerate**: Latest
- **tiktoken**: Latest
- **mcp**: 1.14.1

### Vector Databases & Search
- **chromadb**: 1.0.20
- **opensearch-py**: 2.8.0
- **pymilvus**: 2.5.0
- **qdrant-client**: 1.14.3
- **pinecone**: 6.0.2
- **elasticsearch**: 9.1.0
- **colbert-ai**: 0.2.21

### Document Processing
- **pypdf**: 6.0.0
- **fpdf2**: 2.8.2
- **python-pptx**: 1.0.2
- **docx2txt**: 0.8
- **unstructured**: 0.16.17
- **pypandoc**: 1.15
- **Markdown**: 3.8.2
- **pymdown-extensions**: 10.14.2

### Data Processing
- **pandas**: 2.2.3
- **openpyxl**: 3.1.5
- **pyxlsb**: 1.0.10
- **xlrd**: 2.0.1
- **pyarrow**: 20.0.0

### Image & Audio Processing
- **Pillow**: 11.3.0
- **opencv-python-headless**: 4.11.0.86
- **rapidocr-onnxruntime**: 1.4.4
- **soundfile**: 0.13.1
- **pydub**: Latest
- **faster-whisper**: 1.1.1
- **onnxruntime**: 1.20.1

### Cloud Services
- **boto3**: 1.40.5 (AWS)
- **azure-identity**: 1.25.0
- **azure-storage-blob**: 12.24.1
- **azure-ai-documentintelligence**: 1.0.2
- **google-cloud-storage**: 2.19.0
- **google-api-python-client**: Latest
- **google-auth-httplib2**: Latest
- **google-auth-oauthlib**: Latest

### Utilities & Tools
- **loguru**: 0.7.3
- **APScheduler**: 3.10.4
- **RestrictedPython**: 8.0
- **validators**: 0.35.0
- **psutil**: Latest
- **black**: 25.1.0
- **fake-useragent**: 2.2.0
- **ftfy**: 6.2.3
- **einops**: 0.8.1
- **sentencepiece**: Latest
- **nltk**: 3.9.1
- **rank-bm25**: 0.2.2

### Web Scraping & External APIs
- **youtube-transcript-api**: 1.2.2
- **pytube**: 15.0.0
- **ddgs**: 9.0.0
- **firecrawl-py**: 1.12.0
- **tencentcloud-sdk-python**: 3.0.1336

### Real-time Communication
- **python-socketio**: 5.13.0
- **redis**: Latest
- **pycrdt**: 0.12.25
- **starsessions**: 2.2.1 (with redis extras)

### Testing & Development
- **pytest**: 8.4.1
- **pytest-docker**: 3.1.1
- **playwright**: 1.49.1
- **docker**: 7.1.0

### Observability & Monitoring
- **opentelemetry-api**: 1.36.0
- **opentelemetry-sdk**: 1.36.0
- **opentelemetry-exporter-otlp**: 1.36.0
- **opentelemetry-instrumentation**: 0.57b0
- **opentelemetry-instrumentation-fastapi**: 0.57b0
- **opentelemetry-instrumentation-sqlalchemy**: 0.57b0
- **opentelemetry-instrumentation-redis**: 0.57b0
- **opentelemetry-instrumentation-requests**: 0.57b0
- **opentelemetry-instrumentation-logging**: 0.57b0
- **opentelemetry-instrumentation-httpx**: 0.57b0
- **opentelemetry-instrumentation-aiohttp-client**: 0.57b0

### LDAP Integration
- **ldap3**: 2.9.1

## Configuration Files

### Build & Development Tools
- **package.json**: Main Node.js configuration
- **pyproject.toml**: Python project configuration with Hatch build system
- **uv.lock**: UV package manager lock file
- **requirements.txt**: Python dependencies (backend/)
- **tsconfig.json**: TypeScript configuration
- **vite.config.ts**: Vite build configuration
- **svelte.config.js**: Svelte/SvelteKit configuration

### Code Quality & Formatting
- **.eslintrc.cjs**: ESLint configuration
- **.prettierrc**: Prettier formatting configuration
- **tailwind.config.js**: TailwindCSS configuration
- **postcss.config.js**: PostCSS configuration

### Testing
- **cypress.config.ts**: Cypress E2E testing configuration

### Deployment (Removed)
- **Note**: Docker and Kubernetes files have been removed for local development
- **Alternative**: Direct deployment using npm and Python package managers

### Environment & Git
- **.env.example**: Environment variables template
- **.python-version**: Python version specification
- **.gitignore**: Git ignore patterns

## Build System

### Frontend Build
- **Build Tool**: Vite 5.4.14
- **Package Manager**: npm (with package-lock.json)
- **Module System**: ES Modules
- **Adapter**: Static adapter for deployment

### Backend Build
- **Build System**: Hatch with custom hooks
- **Package Manager**: UV (Ultrafast Python package installer)
- **Lock File**: uv.lock with resolution markers
- **Python Range**: 3.11 to 3.13 (exclusive)

## Development Scripts

### Frontend Scripts
- `npm run dev`: Development server with Pyodide
- `npm run build`: Production build
- `npm run preview`: Preview production build
- `npm run lint`: Run all linting (frontend, types, backend)
- `npm run format`: Format code with Prettier
- `npm run test:frontend`: Run Vitest tests

### Backend Scripts
- Various shell scripts for development and deployment
- Direct Python execution for local development

## Optional Dependencies

### PostgreSQL Support
- **psycopg2-binary**: 2.9.10
- **pgvector**: 0.4.1

### Complete Feature Set
- **pymongo**: Latest
- **moto[s3]**: >=5.0.26
- **gcp-storage-emulator**: >=2024.8.3

## Notes

1. **Version Compatibility**: The project specifies Node.js <=22.x.x but current system has v23.7.0
2. **Python Version**: Project uses 3.12.8 locally for direct development
3. **Package Management**: Uses both npm (frontend) and UV (backend Python packages)
4. **AI Models**: Supports multiple AI providers (OpenAI, Anthropic, Google, etc.)
5. **Vector Databases**: Supports multiple vector database backends
6. **Document Processing**: Comprehensive support for various document formats
7. **Real-time Features**: WebSocket support via Socket.IO
8. **Observability**: Full OpenTelemetry instrumentation
9. **Security**: Multiple authentication methods and security features
10. **Deployment**: Configured for direct local development (Docker/Kubernetes files removed)

## Future Maintenance

This file should be updated whenever:
- Dependencies are added, removed, or updated
- Runtime versions change
- New configuration files are added
- Build system changes
- New optional features are added

Last updated: 2025-09-27
