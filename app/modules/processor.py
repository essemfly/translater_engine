import fitz
import os
import json

from app.external.langchain_client import translate_text
from app.modules.google_document import GoogleDocument
from app.modules.translate_text import replace_text_in_box
from app.utils.dimension import (
    get_paragraph_text,
    get_rect_from_paragraph,
)


def get_ocr_mock_data(pdf: fitz.Document):
    base_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "translater_engine",
        "tests",
    )
    documents_json = os.path.join(
        os.path.join(base_dir, "sample_documents"), "1_document.json"
    )
    documents_data = None
    with open(documents_json, "r") as json_file:  # Open the JSON file
        documents_data = json.load(json_file)

    return documents_data


def process_pdf(pdf: fitz.Document, from_lang: str = "en", to_lang: str = "ko"):
    documents_data = get_ocr_mock_data(pdf)
    pdf_metadata: GoogleDocument = GoogleDocument.from_dict(documents_data)

    for page_number in range(len(pdf)):
        page = pdf[page_number]

        pdf_metadata_dimension = pdf_metadata.pages[page_number].dimension
        pdf_dimension = [page.rect[2], page.rect[3]]

        pdf_metadata_paragraphs = pdf_metadata.pages[page_number].paragraphs
        for paragraph in pdf_metadata_paragraphs:
            text = get_paragraph_text(pdf_metadata, paragraph)
            translatedText = translate_text(from_lang, to_lang, text)
            rect = get_rect_from_paragraph(
                pdf_metadata_dimension, pdf_dimension, paragraph
            )
            new_pdf_doc = replace_text_in_box(pdf, page_number, rect, translatedText)

        break

    return new_pdf_doc


# print('-----'* 10, len(pdf_doc.pages[0].blocks))
# for block in pdf_doc.pages[0].blocks:
#     textPart = block.layout.textAnchor.textSegments[0]
#     print("***", block.layout.boundingPoly)
#     print(pdf_doc.text[int(textPart.startIndex):int(textPart.endIndex)])

# print("-----" * 10, len(pdf_doc.pages[0].paragraphs))
# for paragraph in pdf_doc.pages[0].paragraphs:
#     textPart = paragraph.layout.textAnchor.textSegments[0]
#     print("***", paragraph.layout.boundingPoly)
#     print(pdf_doc.text[int(textPart.startIndex) : int(textPart.endIndex)])

# print('-----'* 10, len(pdf_doc.pages[0].lines))
# for line in pdf_doc.pages[0].lines:
#     textPart = line.layout.textAnchor.textSegments[0]
#     print("***", line.layout.boundingPoly)
#     print(pdf_doc.text[int(textPart.startIndex):int(textPart.endIndex)])
