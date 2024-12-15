import os
from typing import List, TypedDict
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import tempfile

from app.modules.pdf import Paragraph, process_pdf_paragraphs_from_api
from app.modules.save_translated_pdf import save_pdf


pdf_router = APIRouter()


class PDFData(BaseModel):
    original_pdf: str
    ocr_result: str
    translations: list[list[str]] = []
    output_filename: str


class PDFDataV2(BaseModel):
    original_pdf: str
    paragraphs: List[Paragraph]
    output_filename: str


# @pdf_router.post("/process_pdf")
# async def api_process_pdf(data: PDFData):
#     original_pdf = data.original_pdf
#     ocr_result = data.ocr_result
#     output_filename = data.output_filename
#     translations = data.translations

#     if not original_pdf or not ocr_result:
#         raise HTTPException(
#             status_code=400, detail="Both original_pdf and ocr_result must be provided."
#         )

#     # 임시 디렉토리 생성
#     temp_dir = tempfile.mkdtemp()
#     temp_path = os.path.join(temp_dir, "output.pdf")

#     try:
#         new_pdf = process_pdf_from_api(
#             original_pdf, ocr_result, translated_texts=translations
#         )
#         save_pdf(new_pdf, temp_path)

#         return FileResponse(
#             path=temp_path, filename=output_filename, media_type="application/pdf"
#         )
#     except Exception as e:
#         # 에러 발생 시 임시 파일 정리
#         if os.path.exists(temp_path):
#             os.unlink(temp_path)
#         if os.path.exists(temp_dir):
#             os.rmdir(temp_dir)
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         # 응답이 완료된 후 파일 정리를 위한 background task 등록이 필요한 경우
#         # FastAPI의 BackgroundTasks를 사용할 수 있습니다.
#         pass


@pdf_router.post("/process_pdf_v2")
async def api_process_pdf(data: PDFDataV2):
    original_pdf = data.original_pdf
    paragraphs = data.paragraphs
    output_filename = data.output_filename

    # 임시 디렉토리 생성
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, "output.pdf")

    try:
        new_pdf = process_pdf_paragraphs_from_api(
            original_pdf,
            paragraphs,
        )
        save_pdf(new_pdf, temp_path)

        return FileResponse(
            path=temp_path, filename=output_filename, media_type="application/pdf"
        )
    except Exception as e:
        print("Error occured: ", str(e))
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
