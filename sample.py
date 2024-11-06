import json
import os
from datetime import datetime

from app.external.langchain_client import translate_text
from app.modules.google_document import GoogleDocument, GoogleDocumentDimension
from app.modules.load_pdf import load_pdf
from app.modules.save_translated_pdf import save_pdf
from app.modules.translate_text import replace_text_in_box
from app.utils.dimension import normalize_to_pixel_coords


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

    original_pdf_doc = load_pdf(paths["input_pdf"])
    paragraphs = pdf_doc.pages[0].paragraphs
    for paragraph in paragraphs:
        textPart = paragraph.layout.textAnchor.textSegments[0]
        paragraph_text = pdf_doc.text[int(textPart.startIndex) : int(textPart.endIndex)]
        pixel_coords = normalize_to_pixel_coords(
            paragraph.layout.boundingPoly, pageDimension.width, pageDimension.height
        )
        translatedText = translate_text("en", "ko", paragraph_text)
        replace_text_in_box(original_pdf_doc[0], pixel_coords, translatedText)
        print("translatedText", paragraph_text, translatedText)
        break

    print("xxx1")
    save_pdf(original_pdf_doc, paths["output_pdf"])
    print("xxx2")


if __name__ == "__main__":
    main()
