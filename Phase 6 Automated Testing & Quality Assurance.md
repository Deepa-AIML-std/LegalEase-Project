# Phase 6: Automated Testing & Quality Assurance - LegalEase

## 1. Testing Scope
Testing covers application startup, input handling, API communication, AI generation, formatting and failure handling.

## 2. Test Cases
| Test ID | Test | Expected Result |
|---|---|---|
| TC01 | Start FastAPI backend | Server starts on port 8000 |
| TC02 | Start Streamlit frontend | LegalEase UI loads |
| TC03 | Submit valid fields | Request is accepted |
| TC04 | POST `/generate` | Backend receives request |
| TC05 | Gemini available | Draft is generated |
| TC06 | Missing API key | Configuration error is reported |
| TC07 | Gemini temporary 503 | Service-unavailable error is reported |
| TC08 | Document formatting | Sanitized text is formatted correctly |
| TC09 | GitHub security check | Real `.env` is excluded |

## 3. Quality Checks
* Validate required request fields.
* Check backend/frontend connectivity.
* Review generated text before export.
* Check document formatting.
* Keep API credentials outside source control.

## 4. Known External-Service Condition
AI generation depends on the availability of the configured Gemini service. A temporary `503 UNAVAILABLE` response is an external service condition rather than a local application syntax error.
