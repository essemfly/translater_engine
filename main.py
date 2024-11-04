import json
import os
from datetime import datetime

from core.modules.google_document import GoogleDocument
from core.modules.load_pdf import load_pdf


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

    documents_json = os.path.join(paths["document_dir"], "1_document.json")

    documents_data = None
    with open(documents_json, "r") as json_file:  # Open the JSON file
        documents_data = json.load(json_file)

    pdf_doc: GoogleDocument = GoogleDocument.from_dict(documents_data)

    
    # print('-----'* 10, len(pdf_doc.pages[0].blocks))
    # for block in pdf_doc.pages[0].blocks:
    #     textPart = block.layout.textAnchor.textSegments[0]
    #     print("***", block.layout.boundingPoly)
    #     print(pdf_doc.text[int(textPart.startIndex):int(textPart.endIndex)])
    #     return

    # print('-----'* 10, len(pdf_doc.pages[0].paragraphs))
    # for paragraph in pdf_doc.pages[0].paragraphs:
    #     textPart = paragraph.layout.textAnchor.textSegments[0]
    #     print("***", paragraph.layout.boundingPoly)
    #     print(pdf_doc.text[int(textPart.startIndex):int(textPart.endIndex)])
    
    print('-----'* 10, len(pdf_doc.pages[0].lines))
    for line in pdf_doc.pages[0].lines:
        textPart = line.layout.textAnchor.textSegments[0]
        print("***", line.layout.boundingPoly)
        print(pdf_doc.text[int(textPart.startIndex):int(textPart.endIndex)])
    


if __name__ == "__main__":
    main()
