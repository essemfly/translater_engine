import os
from datetime import datetime


from app.modules.load_pdf import load_pdf, load_pdf_all
from app.modules.save_translated_pdf import save_pdf

from app.modules.processor import process_pdf


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
