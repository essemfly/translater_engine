import json
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.external.langchain_client import translate_text
from app.modules.google_document import GoogleDocument
from app.modules.translate_text import replace_text_in_box
from app.utils.dimension import get_paragraph_text, get_rect_from_paragraph
import tempfile
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
    original_pdf = data.original_pdf
    ocr_result = data.ocr_result
    output_filename = data.output_filename
    translations = data.translations

    if not original_pdf or not ocr_result:
        raise HTTPException(
            status_code=400, detail="Both original_pdf and ocr_result must be provided."
        )

    # 임시 디렉토리 생성
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, "output.pdf")

    try:
        new_pdf = process_pdf_from_api(
            original_pdf, ocr_result, translatedTexts=translations
        )
        save_pdf(new_pdf, temp_path)

        return FileResponse(
            path=temp_path, filename=output_filename, media_type="application/pdf"
        )
    except Exception as e:
        # 에러 발생 시 임시 파일 정리
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 응답이 완료된 후 파일 정리를 위한 background task 등록이 필요한 경우
        # FastAPI의 BackgroundTasks를 사용할 수 있습니다.
        pass


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
            rect = get_rect_from_paragraph(
                pdf_metadata_dimension, pdf_dimension, paragraph
            )

            newText = translate_text(text, from_lang, to_lang)
            print("paragraph " + str(idx) + ": ", text, newText)

            new_pdf_doc = replace_text_in_box(
                pdf,
                page_number,
                rect,
                # translatedTexts[idx],
                newText,
            )
        break

    return new_pdf_doc
