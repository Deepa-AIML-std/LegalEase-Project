# Phase 2: Requirement Analysis - LegalEase

## 1. Functional Requirements
* **Document Input Module**: Accept document type, parties, terms and dates.
* **Generation Module**: Send the entered information to the backend `/generate` endpoint.
* **AI Generation Module**: Build a prompt and request a draft from Gemini.
* **Result Module**: Return and display the generated document text.
* **Formatting Module**: Support HTML preview and DOCX/PDF formatting utilities.

## 2. Non-Functional Requirements
* **Usability**: Clean and simple browser-based interface.
* **Maintainability**: Separate frontend, backend, AI and formatting modules.
* **Security**: Store the Gemini API key in `.env`; never expose the real key in GitHub.
* **Error Handling**: Display useful errors for configuration and external AI-service failures.

## 3. Technology Stack Requirements
* **Frontend**: Streamlit.
* **Backend**: Python, FastAPI and Uvicorn.
* **AI Engine**: Google Gemini API.
* **Document Tools**: python-docx and FPDF.
* **Environment**: Python virtual environment, VS Code and Git/GitHub.
