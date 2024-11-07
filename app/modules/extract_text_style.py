import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_path


def convert_pdf_to_image(pdf_path: str, page_num: int) -> np.ndarray:
    images = convert_from_path(pdf_path)
    first_page = images[page_num]
    img = np.array(first_page)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


def extract_text_and_background_colors(img, bounding_box: list) -> dict:
    # bounding_box 좌표 설정
    x_min, y_min, x_max, y_max = bounding_box

    # 텍스트 영역 ROI 설정
    text_roi = img[y_min:y_max, x_min:x_max]

    # 텍스트 색상 계산 (텍스트 영역의 평균 색상)
    text_color = tuple(round(c / 255, 3) for c in cv2.mean(text_roi)[:3])

    # 배경 색상: 텍스트 영역의 바깥쪽 테두리 부분 추출
    border_size = 10  # 바깥쪽에서 샘플링할 영역의 크기
    background_roi = img[
        max(0, y_min - border_size) : min(img.shape[0], y_max + border_size),
        max(0, x_min - border_size) : min(img.shape[1], x_max + border_size),
    ]

    # 텍스트 영역 제외하고 배경 색상 추출
    mask = np.ones(background_roi.shape[:2], dtype="uint8") * 255
    mask[border_size:-border_size, border_size:-border_size] = 0
    background_mean_color = tuple(
        round(c / 255, 3) for c in cv2.mean(background_roi, mask=mask)[:3]
    )

    return {
        "text_color": text_color,  # 텍스트 색상 (0-1 범위의 RGB)
        "background_color": background_mean_color,  # 배경 색상 (0-1 범위의 RGB)
    }
