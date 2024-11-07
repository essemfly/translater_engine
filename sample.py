import json
import os
from datetime import datetime

from app.external.langchain_client import translate_text
from app.modules.google_document import GoogleDocument, GoogleDocumentDimension
from app.modules.load_pdf import load_pdf
from app.modules.save_translated_pdf import save_pdf
from app.modules.translate_text import replace_text_in_box
from app.utils.dimension import (
    calculate_rect_from_coords,
    normalize_to_point_coords,
    scale_coords_to_pdf_points,
)


def main():
    base_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "translater_engine",
        "tests",
    )
    paths = {
        "input_pdf": os.path.join(base_dir, "sample_files", "1.pdf"),
        "document_dir": os.path.join(base_dir, "sample_documents"),
        "output_dir": os.path.join(base_dir, "sample_outputs"),
        "output_pdf": os.path.join(
            base_dir,
            "sample_outputs",
            f'output_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
        ),
    }

    os.makedirs(paths["output_dir"], exist_ok=True)

    # pdf를 분석해서 만들어진 object
    documents_json = os.path.join(paths["document_dir"], "1_document.json")

    documents_data = None
    with open(documents_json, "r") as json_file:  # Open the JSON file
        documents_data = json.load(json_file)

    pdf_doc: GoogleDocument = GoogleDocument.from_dict(documents_data)

    pageDimension = pdf_doc.pages[0].dimension
    print("dimension", pageDimension)

    original_pdf_doc = load_pdf(paths["input_pdf"])
    new_pdf_doc = load_pdf(paths["input_pdf"])
    page_number = 0

    print("pymupdf dimension: ", original_pdf_doc[page_number].rect)
    pdf_width = original_pdf_doc[page_number].rect[2]
    pdf_height = original_pdf_doc[page_number].rect[3]

    paragraphs = pdf_doc.pages[page_number].paragraphs
    for paragraph in paragraphs:
        textPart = paragraph.layout.textAnchor.textSegments[0]
        paragraph_text = pdf_doc.text[int(textPart.startIndex) : int(textPart.endIndex)]

        print("dimension", pageDimension)
        source_coords = normalize_to_point_coords(
            paragraph.layout.boundingPoly, pageDimension.width, pageDimension.height
        )
        temp = calculate_rect_from_coords(source_coords)
        output_rect = scale_coords_to_pdf_points(
            temp,
            source_width=pageDimension.width,
            source_height=pageDimension.height,
            target_width=pdf_width,
            target_height=pdf_height,
        )
        print("### point cords", output_rect)

        # translatedText = translate_text("en", "ko", paragraph_text)
        translatedText = "이 계약서와 이에 따라 발행 가능한 어떠한 증권도 1933년 증권법(변경된 “증권법”) 또는 특정 주의 증권법에 따라 등록되지 않았습니다. 이러한 증권은 해당 법과 적용 가능한 주 증권법에 따라 허용되는 한, 효력 있는 등록서를 가지거나 그에 대한 면제를 받아서만 제안, 판매 또는 다른 방식으로 양도, 담보 제공 또는 저당권 설정이 가능합니다."

        new_pdf_doc = replace_text_in_box(
            original_pdf_doc, page_number, output_rect, translatedText
        )
        break

    print("xxx1")
    save_pdf(new_pdf_doc, paths["output_pdf"])
    print("xxx2")


if __name__ == "__main__":
    main()


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
