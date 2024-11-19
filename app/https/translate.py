import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.external.langchain_client import translate_text
from app.modules.google_document import GoogleDocument
from app.modules.translate_text import replace_text_in_box
from app.utils.dimension import get_paragraph_text, get_rect_from_paragraph

from app.modules.save_translated_pdf import save_pdf
from app.modules.load_pdf import load_pdf_all


pdf_router = APIRouter()


class PDFData(BaseModel):
    original_pdf: str
    ocr_result: str
    translations: list[str] = []
    output_filename: str


@pdf_router.post("/process_pdf")
async def api_process_pdf(data: PDFData):
    # 예시 처리: 데이터를 로깅하거나 저장할 수 있습니다.
    original_pdf = data.original_pdf
    ocr_result = data.ocr_result
    output_filename = data.output_filename
    translations = data.translations

    output_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "tests",
        "sample_outputs",
        output_filename,
    )

    new_pdf = process_pdf_from_api(
        original_pdf, ocr_result, translatedTexts=translations
    )
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
    pdf_url: str,
    metadata: str,
    from_lang: str = "en",
    to_lang: str = "ko",
    translatedTexts: list[str] = [],
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
            print("paragraph " + str(idx) + ": ", text, translatedTexts[idx])
            rect = get_rect_from_paragraph(
                pdf_metadata_dimension, pdf_dimension, paragraph
            )

            new_pdf_doc = replace_text_in_box(
                pdf,
                page_number,
                rect,
                translatedTexts[idx],
            )
        break

    return new_pdf_doc
