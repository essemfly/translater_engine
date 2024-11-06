import fitz


def save_pdf(pdf_document: fitz.Document, output_path: str) -> bool:
    """수정된 PDF를 저장하는 함수

    Args:
        pdf_document (fitz.Document): PDF 문서 객체
        output_path (str): 저장할 파일 경로

    Returns:
        bool: 성공 여부
    """
    try:
        pdf_document.save(output_path)
        pdf_document.close()
        return True
    except Exception as e:
        print(f"PDF 저장 중 오류 발생: {e}")
        return False
