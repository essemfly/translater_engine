import json
from app.modules.google_document import GoogleDocument
from app.modules.load_pdf import load_pdf_all
from app.modules.translate_text import replace_text_in_box
from app.utils.dimension import get_rect_from_paragraph


def process_pdf_from_api(
    pdf_url: str,
    metadata: str,
    from_lang: str = "en",
    to_lang: str = "ko",
    translated_texts: list[list[str]] = [],
):
    pdf = load_pdf_all(url=pdf_url)
    json_metadata = json.loads(metadata)
    pdf_metadata: GoogleDocument = GoogleDocument.from_dict(json_metadata)

    for page_number in range(len(pdf)):
        page = pdf[page_number]

        pdf_metadata_dimension = pdf_metadata.pages[page_number].dimension
        print("pdf_metadata_dimension: ", pdf_metadata_dimension)
        pdf_dimension = [page.rect[2], page.rect[3]]
        print("pdf_dimension: ", pdf_dimension)

        pdf_metadata_paragraphs = pdf_metadata.pages[page_number].paragraphs
        for idx, paragraph in enumerate(pdf_metadata_paragraphs):
            # text = get_paragraph_text(pdf_metadata, paragraph)
            # print(
            #     "paragraph " + str(idx) + ": ", text, translated_texts[page_number][idx]
            # )

            refined_text = translated_texts[page_number][idx].replace("\n", "")
            rect = get_rect_from_paragraph(
                pdf_metadata_dimension, pdf_dimension, paragraph
            )
            new_pdf_doc = replace_text_in_box(pdf, page_number, rect, refined_text)

    return new_pdf_doc