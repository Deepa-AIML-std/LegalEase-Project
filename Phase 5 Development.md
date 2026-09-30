# Phase 5: Development - LegalEase

## 1. Technology Stack
* Python
* Streamlit
* FastAPI
* Uvicorn
* Google Gemini API
* python-dotenv
* python-docx
* FPDF

## 2. Backend Development
The backend exposes a `POST /generate` endpoint and validates:
* `document_type`
* `parties`
* `terms`
* `dates`

The route passes these values to `GeminiDocumentGenerator` and returns the generated document text.

## 3. AI Generation
`gemini_generator.py`:
1. Loads environment variables.
2. Reads `GEMINI_API_KEY`.
3. Creates the Gemini client.
4. Builds a legal-document drafting prompt.
5. Requests generated content.
6. Returns the cleaned response text.

## 4. Frontend Development
`frontend/app.py`:
* collects document details,
* sends the JSON request to the backend,
* receives the generated response,
* displays the result,
* provides document preview/output functions.

## 5. Document Formatting
`formatters.py` contains utilities for:
* text sanitization,
* HTML preview,
* DOCX formatting,
* PDF formatting.

## 6. Security
The real `.env` file and API key must remain local and must not be uploaded to GitHub. `.env.example` can be included as a safe configuration template.
