import cv2
import numpy as np
from PIL import Image


def extract_text_and_background_colors(image_path: str, bounding_box: list) -> dict:
    """
    이미지에서 주어진 bounding box로 텍스트 색상 및 배경색 추출.

    Args:
        image_path (str): 이미지 파일 경로
        bounding_box (list): [좌상단 x, y, 우하단 x, y] 좌표 리스트

    Returns:
        dict: 텍스트 색상 및 배경색 정보
    """
    # 이미지 로드
    img = cv2.imread(image_path)

    # bounding_box 좌표 설정
    x_min, y_min, x_max, y_max = bounding_box

    # 텍스트 영역 ROI 설정
    text_roi = img[y_min:y_max, x_min:x_max]

    # 텍스트 색상 계산 (텍스트 영역의 평균 색상)
    text_color = cv2.mean(text_roi)[:3]

    # 배경 색상: 텍스트 영역의 바깥쪽 테두리 부분 추출
    border_size = 10  # 바깥쪽에서 샘플링할 영역의 크기
    background_roi = img[
        max(0, y_min - border_size) : min(img.shape[0], y_max + border_size),
        max(0, x_min - border_size) : min(img.shape[1], x_max + border_size),
    ]

    # 텍스트 영역 제외하고 배경 색상 추출
    mask = np.ones(background_roi.shape[:2], dtype="uint8") * 255
    mask[border_size:-border_size, border_size:-border_size] = (
        0  # 중심부는 0으로, 바깥쪽만 남기기
    )
    background_mean_color = cv2.mean(background_roi, mask=mask)[:3]

    return {
        "text_color": text_color,  # 텍스트 색상 (RGB)
        "background_color": background_mean_color,  # 배경 색상 (RGB)
    }
