from app.modules.load_pdf import load_pdf_all
from app.modules.translate_text import replace_text_in_box
from typing import List, TypedDict


class Paragraph(TypedDict):
    pageNum: int
    boundingBox: List[str]  # [x0, y0, x1, y1]
    translatedText: str
    style: str


def process_pdf_paragraphs_from_api(
    pdf_url: str,
    paragraphs: List[Paragraph],
    from_lang: str = "en",
    to_lang: str = "ko",
    page_number_limit: int = 15,
):
    """
    Process PDF with given paragraphs and translations

    Args:
        pdf_url (str): URL of the PDF to process
        paragraphs (List[Paragraph]): List of paragraphs with bounding boxes and translations
        from_lang (str, optional): Source language. Defaults to "en"
        to_lang (str, optional): Target language. Defaults to "ko"
        page_number (int, optional): Page number to process. Defaults to 1

    Returns:
        PDF document with replaced text
    """
    # Load PDF
    pdf = load_pdf_all(url=pdf_url)

    for page_number in range(1, len(pdf) + 1):
        if page_number > page_number_limit:
            break

        page = pdf[page_number - 1]
        pdf_dimension = [page.rect[2], page.rect[3]]

        # Process each paragraph
        for paragraph in paragraphs:

            if paragraph["pageNum"] != page_number:
                continue
            bounding = paragraph["boundingBox"]
            translated_text = paragraph["translatedText"]

            # Convert bounding box coordinates if needed
            # This assumes the bounding coordinates are in the same scale as pdf_dimension
            rect = [float(value) for value in bounding]

            # Replace text in the PDF
            pdf = replace_text_in_box(pdf, page_number, rect, translated_text)

    return pdf
