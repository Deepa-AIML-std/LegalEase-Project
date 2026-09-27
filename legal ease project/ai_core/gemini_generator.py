import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


class GeminiDocumentGenerator:
    """
    Generates legal-document drafts using Google Gemini.

    MOCK_AI=false can be used to test the application without
    making an external Gemini API request.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        mock_value = os.getenv("MOCK_AI", "false").lower()
        self.mock_ai = mock_value in {
            "true",
            "1",
            "yes",
            "on"
        }

        self.client = None

        if not self.mock_ai:
            if not self.api_key:
                raise ValueError(
                    "GEMINI_API_KEY is missing. "
                    "Add it to your .env file or set MOCK_AI=true."
                )

            from google import genai

            self.client = genai.Client(
                api_key=self.api_key
            )

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: List[str],
        effective_date: str,
        jurisdiction: str = "",
        additional_instructions: str = ""
    ) -> str:

        if self.mock_ai:
            return self._mock_document(
                document_type=document_type,
                parties=parties,
                terms=terms,
                effective_date=effective_date,
                jurisdiction=jurisdiction,
                additional_instructions=additional_instructions
            )

        prompt = self._build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date,
            jurisdiction=jurisdiction,
            additional_instructions=additional_instructions
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            print("--- GENERATED DOCUMENT OUTPUT ---")
            print(text.strip())
            return text.strip()
        except Exception as exc:
            raise RuntimeError(
                f"Gemini generation failed: {exc}"
            ) from exc

    def _build_prompt(
        self,
        document_type: str,
        parties: str,
        terms: List[str],
        effective_date: str,
        jurisdiction: str,
        additional_instructions: str
    ) -> str:

        terms_text = "\n".join(
            f"- {term}" for term in terms
        )

        jurisdiction_text = (
            jurisdiction
            if jurisdiction
            else "Not specified"
        )

        instructions_text = (
            additional_instructions
            if additional_instructions
            else "None"
        )

        return f"""
You are a legal-document drafting assistant.

Create a structured draft of the requested legal document.

IMPORTANT:
- This is a drafting assistant, not a lawyer.
- Do not claim that the document is legally valid or guaranteed.
- Do not invent facts that were not provided.
- Clearly mark missing information as [TO BE COMPLETED].
- Use professional and clear language.
- Use headings and numbered sections.
- Include the provided terms.
- Do not include Markdown code fences.
- Return only the document itself.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{effective_date}

JURISDICTION:
{jurisdiction_text}

TERMS AND CONDITIONS:
{terms_text}

ADDITIONAL INSTRUCTIONS:
{instructions_text}

Create the document with this general structure where appropriate:

TITLE

PARTIES

EFFECTIVE DATE

RECITALS / BACKGROUND

1. PURPOSE
2. DEFINITIONS
3. OBLIGATIONS
4. PAYMENT / CONSIDERATION
5. CONFIDENTIALITY
6. INTELLECTUAL PROPERTY
7. TERM AND TERMINATION
8. LIABILITY
9. DISPUTE RESOLUTION
10. GOVERNING LAW
11. GENERAL PROVISIONS

SIGNATURES

Use only sections relevant to the selected document type.
"""

    def _mock_document(
        self,
        document_type: str,
        parties: str,
        terms: List[str],
        effective_date: str,
        jurisdiction: str,
        additional_instructions: str
    ) -> str:

        terms_text = "\n".join(
            f"- {term}" for term in terms
        )

        jurisdiction_text = (
            jurisdiction
            if jurisdiction
            else "[TO BE COMPLETED]"
        )

        instructions_text = (
            additional_instructions
            if additional_instructions
            else "None"
        )

        return f"""
{document_type.upper()}

PARTIES

{parties}

EFFECTIVE DATE

{effective_date}

1. PURPOSE

This document records the agreement between the parties identified above
for the purpose described by the selected document type.

2. TERMS AND CONDITIONS

The parties agree to the following terms:

{terms_text}

3. RESPONSIBILITIES

Each party shall perform the responsibilities agreed upon by the parties
and described in this document.

4. CONFIDENTIALITY

Where confidential information is exchanged, the parties shall take
reasonable steps to protect such information from unauthorized disclosure.

5. TERM AND TERMINATION

This agreement shall begin on the effective date stated above and shall
continue according to the agreed terms.

6. GOVERNING LAW

Jurisdiction:

{jurisdiction_text}

7. ADDITIONAL INSTRUCTIONS

{instructions_text}

8. GENERAL PROVISIONS

Any amendments to this document should be made in writing and agreed to
by the relevant parties.

SIGNATURES

Party 1: ______________________________

Name: __________________________________

Date: __________________________________


Party 2: ______________________________

Name: __________________________________

Date: __________________________________


LEGAL NOTICE

This document is an AI-generated draft provided for informational and
drafting purposes. It should be reviewed by a qualified legal
professional before being signed or relied upon.
""".strip()