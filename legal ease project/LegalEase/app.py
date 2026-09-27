import html
import os
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv

from services.document_export import (
    format_docx,
    format_pdf,
    format_txt
)


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #777;
        margin-bottom: 30px;
    }

    .preview-box {
        background-color: #111827;
        color: #f9fafb;
        padding: 25px;
        border-radius: 12px;
        height: 600px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-family: Georgia, serif;
        line-height: 1.6;
    }

    .info-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f3f4f6;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True
)


with st.sidebar:

    st.header("Settings")

    st.write(
        "Create, edit and export structured legal-document drafts."
    )

    st.divider()

    st.write(
        "**Backend:**"
    )

    st.code(
        BACKEND_URL
    )

    st.divider()

    st.caption(
        "LegalEase generates AI-assisted drafts. "
        "Review important legal documents with a qualified "
        "legal professional before signing or relying on them."
    )


if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""


if "edited_document" not in st.session_state:
    st.session_state.edited_document = ""


if "show_editor" not in st.session_state:
    st.session_state.show_editor = False


left, right = st.columns(
    [1, 1.3],
    gap="large"
)


with left:

    st.subheader("Document Details")

    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Lease Agreement",
            "Non-Disclosure Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "Employment Offer Letter",
            "Partnership Agreement",
            "General Agreement"
        ]
    )


    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Example:\n"
            "Jane Doe (Service Provider)\n"
            "TechNova Inc. (Client)"
        ),
        height=120
    )


    effective_date = st.date_input(
        "Effective Date",
        value=date.today()
    )


    jurisdiction = st.text_input(
        "Jurisdiction",
        placeholder="Example: Tamil Nadu, India"
    )


    terms_text = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Enter one term per line.\n\n"
            "Example:\n"
            "Payment must be made within 30 days.\n"
            "Confidentiality must be maintained.\n"
            "Either party may terminate with 15 days notice."
        ),
        height=180
    )


    additional_instructions = st.text_area(
        "Additional Instructions",
        placeholder=(
            "Optional instructions for the AI..."
        ),
        height=100
    )


    generate_button = st.button(
        "Generate Document",
        type="primary",
        use_container_width=True
    )


    if generate_button:

        if not parties.strip():

            st.error(
                "Please enter the parties involved."
            )

        elif not terms_text.strip():

            st.error(
                "Please enter at least one term."
            )

        else:

            terms = [
                term.strip()
                for term in terms_text.splitlines()
                if term.strip()
            ]

            payload = {
                "document_type": document_type,
                "parties": parties.strip(),
                "terms": terms,
                "effective_date": effective_date.strftime(
                    "%d/%m/%Y"
                ),
                "jurisdiction": jurisdiction.strip(),
                "additional_instructions":
                    additional_instructions.strip()
            }

            try:

                with st.spinner(
                    "Generating your legal document..."
                ):

                    response = requests.post(
                        f"{BACKEND_URL}/generate",
                        json=payload,
                        timeout=120
                    )


                if response.status_code == 200:

                    data = response.json()

                    generated = data.get(
                        "document",
                        ""
                    )

                    st.session_state.generated_document = generated

                    st.session_state.edited_document = generated

                    st.session_state.show_editor = False

                    st.success(
                        "Document generated successfully."
                    )

                else:

                    try:
                        error_data = response.json()
                        message = error_data.get(
                            "detail",
                            response.text
                        )
                    except Exception:
                        message = response.text

                    st.error(
                        f"Backend error: {message}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to FastAPI. "
                    "Make sure the backend is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. "
                    "Try again."
                )

            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )


with right:

    st.subheader("Document Preview")


    if st.session_state.generated_document:

        document = (
            st.session_state.edited_document
            if st.session_state.show_editor
            else st.session_state.generated_document
        )


        if st.session_state.show_editor:

            edited = st.text_area(
                "Edit your document",
                value=st.session_state.edited_document,
                height=600
            )

            st.session_state.edited_document = edited

            if st.button(
                "Save Changes",
                use_container_width=True
            ):

                st.session_state.generated_document = edited

                st.session_state.edited_document = edited

                st.session_state.show_editor = False

                st.rerun()


        else:

            safe_document = html.escape(
                document
            )

            st.markdown(
                f"""
                <div class="preview-box">
                {safe_document}
                </div>
                """,
                unsafe_allow_html=True
            )


            st.write("")


            if st.button(
                "Click to Edit Document",
                use_container_width=True
            ):

                st.session_state.edited_document = document

                st.session_state.show_editor = True

                st.rerun()


        st.divider()

        st.subheader("Download")


        final_document = (
            st.session_state.edited_document
        )


        txt_data = format_txt(
            final_document
        )

        docx_data = format_docx(
            final_document,
            document_type
        )

        pdf_data = format_pdf(
            final_document,
            document_type
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.download_button(
                label="Download TXT",
                data=txt_data,
                file_name="LegalEase_Document.txt",
                mime="text/plain",
                use_container_width=True
            )


        with col2:

            st.download_button(
                label="Download DOCX",
                data=docx_data,
                file_name="LegalEase_Document.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True
            )


        with col3:

            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name="LegalEase_Document.pdf",
                mime="application/pdf",
                use_container_width=True
            )


    else:

        st.info(
            "Your generated document will appear here."
        )

        st.markdown(
            """
            <div class="info-box">

            <b>How it works</b>

            <br><br>

            1. Select a document type.<br>
            2. Enter the parties.<br>
            3. Enter the effective date.<br>
            4. Add terms and conditions.<br>
            5. Click Generate Document.<br>
            6. Review and edit the result.<br>
            7. Download as TXT, DOCX or PDF.

            </div>
            """,
            unsafe_allow_html=True
        )
