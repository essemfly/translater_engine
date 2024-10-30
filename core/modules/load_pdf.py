import fitz  # PyMuPDF
import os
from pdf2image import convert_from_path


def load_pdf(file_path: str) -> fitz.Document:
    """PDF 파일을 로드하는 함수

    Args:
        file_path (str): PDF 파일 경로

    Returns:
        fitz.Document: 로드된 PDF 문서 객체
    """
    try:
        pdf_document = fitz.open(file_path)
        return pdf_document
    except Exception as e:
        print(f"PDF 로드 중 오류 발생: {e}")
        return None


def pdf_to_images(pdf_path: str, output_folder: str) -> list:
    """
    PDF 파일을 페이지별로 PNG 이미지로 변환.
    Args:
        pdf_path (str): 변환할 PDF 파일의 경로
        output_folder (str): 이미지를 저장할 폴더 경로
    Returns:
        list: 생성된 이미지 파일의 경로 리스트
    """
    images = convert_from_path(pdf_path, fmt="png")
    image_paths = []

    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(image_path, "PNG")
        image_paths.append(image_path)

    return image_paths
