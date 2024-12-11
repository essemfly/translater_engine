import json
from app.modules.load_pdf import load_pdf_all
from app.modules.translate_text import (
    replace_text_in_box,
    replace_text_in_box_single_line,
    replace_text_in_box_with_align,
)
from typing import List, TypedDict


class Paragraph(TypedDict):
    pageNum: int
    boundingBox: List[str]  # [x0, y0, x1, y1]
    originalText: str
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
            font_properties = json.loads(paragraph["style"])

            fontSize = font_properties.get("fontSize", 11)
            color = font_properties.get("color", [0, 0, 0])
            bgColor = font_properties.get(
                "bgColor", [255, 255, 255]
            )
            font = font_properties.get(
                "font", "Helvetica"
            )  # Assuming Helvetica as default font
            isBold = font_properties.get("isBold", False)
            isItalic = font_properties.get("isItalic", False)

            # 딕셔너리 값들을 순서대로 리스트로 변환
            color = [float(val) / 255.0 for val in color]
            bgColor = [float(val) / 255.0 for val in bgColor]

            # 폰트 이름 조정
            if isBold:
                font_name = font + "-Bold"  # Bold 폰트 이름 조정
            else:
                font_name = font

            if isItalic:
                font_name += "-Italic"  # Italic 폰트 이름 조정

            # Convert bounding box coordinates if needed
            rect = [float(value) for value in bounding]

            print(f"Processing : ", fontSize, font_name, color, translated_text, rect)
            # Replace text in the PDF
            pdf = replace_text_in_box_single_line(
                pdf,
                page_number,
                rect,
                translated_text,
                fontSize,
                font_name,
                color,
                bgColor,
            )

    return pdf
