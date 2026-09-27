from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_core.gemini_generator import GeminiDocumentGenerator


router = APIRouter()

generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=3000
    )

    terms: List[str] = Field(
        default_factory=list,
        max_length=50
    )

    effective_date: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    jurisdiction: str = Field(
        default="",
        max_length=300
    )

    additional_instructions: str = Field(
        default="",
        max_length=3000
    )


@router.post("/generate")
def generate_document(
    request: DocumentRequest
):

    try:

        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            jurisdiction=request.jurisdiction,
            additional_instructions=request.additional_instructions
        )

        return {
            "success": True,
            "document_type": request.document_type,
            "document": document
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )