# import fitz
# import os
# import json

# from app.external.langchain_client import translate_text
# from app.modules.google_document import GoogleDocument
# from app.modules.load_pdf import load_pdf, load_pdf_all
# from app.modules.translate_text import (
#     replace_text_in_box,
#     replace_text_in_box_with_align,
# )
# from app.utils.dimension import (
#     get_paragraph_text,
#     get_rect_from_paragraph,
#     get_rect_style_from_paragraph,
# )


# def get_ocr_mock_data(documents_json_path):
#     documents_json = os.path.join(documents_json_path, "3_document.json")
#     documents_data = None
#     with open(documents_json, "r") as json_file:  # Open the JSON file
#         documents_data = json.load(json_file)

#     return documents_data


# def process_pdf(pdf_path: str, from_lang: str = "en", to_lang: str = "ko"):
#     pdf = load_pdf(pdf_path)
#     documents_data = get_ocr_mock_data(
#         "/Users/seokmin/Desktop/translater_engine/tests/sample_documents"
#     )
#     pdf_metadata: GoogleDocument = GoogleDocument.from_dict(documents_data)

#     for page_number in range(len(pdf)):
#         page = pdf[page_number]

#         pdf_metadata_dimension = pdf_metadata.pages[page_number].dimension
#         pdf_dimension = [page.rect[2], page.rect[3]]

#         pdf_metadata_paragraphs = pdf_metadata.pages[page_number].paragraphs
#         for idx, paragraph in enumerate(pdf_metadata_paragraphs):
#             text = get_paragraph_text(pdf_metadata, paragraph)
#             translatedText = translate_text(from_lang, to_lang, text)
#             print("paragraph " + str(idx) + ": ", text, translatedText)
#             rect = get_rect_from_paragraph(
#                 pdf_metadata_dimension, pdf_dimension, paragraph
#             )

#             text_style = get_rect_style_from_paragraph(
#                 pdf_path, page_number, paragraph, pdf_metadata_dimension
#             )

#             # print("text style", text_style)
#             new_pdf_doc = replace_text_in_box(
#                 pdf,
#                 page_number,
#                 rect,
#                 translatedText,
#                 text_color=text_style["text_color"],
#                 bg_color=text_style["bg_color"],
#             )
#             # new_pdf_doc = replace_text_in_box_with_align(
#             #     pdf,
#             #     page_number,
#             #     rect,
#             #     translatedText,
#             #     align="left",
#             # )

#         break

#     return new_pdf_doc


# # print('-----'* 10, len(pdf_doc.pages[0].blocks))
# # for block in pdf_doc.pages[0].blocks:
# #     textPart = block.layout.textAnchor.textSegments[0]
# #     print("***", block.layout.boundingPoly)
# #     print(pdf_doc.text[int(textPart.startIndex):int(textPart.endIndex)])

# # print("-----" * 10, len(pdf_doc.pages[0].paragraphs))
# # for paragraph in pdf_doc.pages[0].paragraphs:
# #     textPart = paragraph.layout.textAnchor.textSegments[0]
# #     print("***", paragraph.layout.boundingPoly)
# #     print(pdf_doc.text[int(textPart.startIndex) : int(textPart.endIndex)])

# # print('-----'* 10, len(pdf_doc.pages[0].lines))
# # for line in pdf_doc.pages[0].lines:
# #     textPart = line.layout.textAnchor.textSegments[0]
# #     print("***", line.layout.boundingPoly)
# #     print(pdf_doc.text[int(textPart.startIndex):int(textPart.endIndex)])
