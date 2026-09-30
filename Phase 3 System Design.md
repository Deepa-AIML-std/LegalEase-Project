# Phase 3: System Design - LegalEase

## 1. System Architecture Pattern
LegalEase follows a modular client-server style architecture.

* **Client Layer**: Streamlit frontend in `frontend/app.py`.
* **Server Layer**: FastAPI backend in `backend/main.py` and `backend/routes.py`.
* **AI Intelligence Layer**: `backend/ai_core/gemini_generator.py`.
* **Document Layer**: `backend/document_utils/formatters.py`.

## 2. Architectural Workflow Design
1. User enters document details in the Streamlit interface.
2. Frontend sends a JSON request to the FastAPI `/generate` endpoint.
3. FastAPI validates the request.
4. GeminiDocumentGenerator creates the AI prompt and calls Gemini.
5. Generated text is returned to the backend.
6. Frontend displays the generated draft and formatting/output options.

## 3. Component Interaction Diagram Flow
```text
[Streamlit UI]
      |
      | POST /generate
      v
[FastAPI Backend]
      |
      | AI request
      v
[Gemini API]
      |
      | Generated text
      v
[FastAPI Backend]
      |
      | JSON response
      v
[Streamlit UI]
      |
      v
[Preview / DOCX / PDF]
```

## 4. Project Structure
```text
LegalEase/
├── backend/
│   ├── ai_core/
│   │   └── gemini_generator.py
│   ├── document_utils/
│   │   └── formatters.py
│   ├── main.py
│   └── routes.py
├── frontend/
│   └── app.py
├── assets/
├── .env
├── .env.example
├── requirements.txt
└── README.md
```
