import fitz  # PyMuPDF


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
