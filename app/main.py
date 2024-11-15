import json
import os
from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from openai import BaseModel

from app.external.langchain_client import translate_text
from app.modules.google_document import GoogleDocument
from app.modules.load_pdf import load_pdf_all
from app.modules.save_translated_pdf import save_pdf
from app.modules.translate_text import replace_text_in_box
from app.utils.dimension import (
    get_paragraph_text,
    get_rect_from_paragraph,
)


app = FastAPI(
    title="My FastAPI Application",
    description="A simple FastAPI application with SQLAlchemy and Alembic.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # 모든 도메인에 대해 허용. 필요한 경우 특정 도메인으로 제한 가능.
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


class PDFData(BaseModel):
    original_pdf: str
    ocr_result: str
    output_filename: str


@app.post("/process_pdf")
async def api_process_pdf(data: PDFData):
    # 예시 처리: 데이터를 로깅하거나 저장할 수 있습니다.
    original_pdf = data.original_pdf
    ocr_result = data.ocr_result
    output_filename = data.output_filename

    output_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "tests",
        "sample_outputs",
        output_filename
    )
        
    new_pdf = process_pdf_from_api(original_pdf, ocr_result)
    print("New PDF created:", new_pdf)

    save_pdf(new_pdf, output_path)


    # 필요에 따라 예외 처리도 추가 가능
    if not original_pdf or not ocr_result:
        raise HTTPException(
            status_code=400, detail="Both original_pdf and ocr_result must be provided."
        )

    # 실제 로직을 여기에 추가
    return {
        "message": "PDF processed successfully",
        "path": output_path,
    }


def process_pdf_from_api(
    pdf_url: str, metadata: str, from_lang: str = "en", to_lang: str = "ko"
):
    pdf = load_pdf_all(url=pdf_url)

    json_metadata = json.loads(metadata)
    pdf_metadata: GoogleDocument = GoogleDocument.from_dict(json_metadata)

    for page_number in range(len(pdf)):
        page = pdf[page_number]

        pdf_metadata_dimension = pdf_metadata.pages[page_number].dimension
        pdf_dimension = [page.rect[2], page.rect[3]]

        pdf_metadata_paragraphs = pdf_metadata.pages[page_number].paragraphs
        for idx, paragraph in enumerate(pdf_metadata_paragraphs):
            text = get_paragraph_text(pdf_metadata, paragraph)
            translatedText = translate_text(from_lang, to_lang, text)
            print("paragraph " + str(idx) + ": ", text, translatedText)
            rect = get_rect_from_paragraph(
                pdf_metadata_dimension, pdf_dimension, paragraph
            )

            new_pdf_doc = replace_text_in_box(
                pdf,
                page_number,
                rect,
                translatedText,
            )
        break

    return new_pdf_doc
