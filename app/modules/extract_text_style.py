import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
from collections import Counter
from sklearn.cluster import KMeans


def convert_pdf_to_image(pdf_path: str, page_num: int) -> np.ndarray:
    images = convert_from_path(pdf_path)
    first_page = images[page_num]
    img = np.array(first_page)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter

def get_dominant_colors(roi, n_colors=2, min_pixels=10):
    """
    이미지 영역에서 대표 색상을 추출하는 함수
    
    Args:
        roi: 관심 영역 이미지
        n_colors: 추출할 색상 수
        min_pixels: 최소 필요 픽셀 수
    """
    # 픽셀 수가 너무 적은 경우 처리
    if len(roi) < min_pixels:
        if len(roi) == 0:
            return None
        # 픽셀이 적을 경우 평균값 사용
        return [np.mean(roi, axis=0)]
    
    try:
        pixels = roi.reshape(-1, 3)
        kmeans = KMeans(n_clusters=min(n_colors, len(pixels)), 
                       random_state=42, 
                       n_init=10)
        kmeans.fit(pixels)
        
        colors = kmeans.cluster_centers_
        labels = kmeans.labels_
        count = Counter(labels)
        
        colors = [(count[i], colors[i]) for i in range(len(colors))]
        colors.sort(reverse=True)
        
        return [c[1] for c in colors]
    except Exception as e:
        # 클러스터링 실패 시 평균값 사용
        return [np.mean(roi, axis=0)]

def extract_text_and_background_colors(img, bounding_box: list) -> dict:
    """
    텍스트 영역과 배경의 대표 색상을 추출하는 함수
    """
    x_min, y_min, x_max, y_max = bounding_box
    
    # 유효한 좌표 범위 확인 및 보정
    x_min = max(0, x_min)
    y_min = max(0, y_min)
    x_max = min(img.shape[1], x_max)
    y_max = min(img.shape[0], y_max)
    
    # 영역이 너무 작은 경우 처리
    if x_max - x_min < 2 or y_max - y_min < 2:
        return {
            "text_color": (0, 0, 0),  # 기본값
            "background_color": (1, 1, 1),  # 기본값
            "confidence_score": 21.0,  # 최대 대비값
            "method_used": "fallback_size_too_small"
        }
    
    # 텍스트 영역 추출
    text_roi = img[y_min:y_max, x_min:x_max]
    
    # 패딩을 포함한 더 넓은 영역 추출
    padding = max(1, int(min(text_roi.shape[0], text_roi.shape[1]) * 0.2))
    padded_bbox = [
        max(0, x_min - padding),
        max(0, y_min - padding),
        min(img.shape[1], x_max + padding),
        min(img.shape[0], y_max + padding)
    ]
    padded_roi = img[padded_bbox[1]:padded_bbox[3], padded_bbox[0]:padded_bbox[2]]
    
    # 엣지 검출 시도
    try:
        gray_text = cv2.cvtColor(text_roi, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_text, (3, 3), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        # 텍스트가 검출되지 않은 경우 임계값 조정
        if np.sum(edges) == 0:
            edges = cv2.Canny(blurred, 30, 100)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        text_mask = cv2.dilate(edges, kernel, iterations=2)
        
        # 마스크로 텍스트와 배경 분리
        text_pixels = text_roi[text_mask > 0]
        background_pixels = text_roi[text_mask == 0]
        
        # 텍스트나 배경 픽셀이 충분하지 않은 경우 대체 방법 사용
        if len(text_pixels) < 10 or len(background_pixels) < 10:
            raise ValueError("Insufficient pixels detected")
            
        # 색상 추출
        text_colors = get_dominant_colors(text_pixels, n_colors=1)
        bg_colors = get_dominant_colors(background_pixels, n_colors=1)
        
        if text_colors is None or bg_colors is None:
            raise ValueError("Color extraction failed")
            
        method = "edge_detection"
        
    except Exception as e:
        # 엣지 검출 실패 시 대체 방법 사용
        try:
            # 밝기 기반 이진화 시도
            gray = cv2.cvtColor(text_roi, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            text_pixels = text_roi[binary > 127]
            background_pixels = text_roi[binary <= 127]
            
            text_colors = get_dominant_colors(text_pixels, n_colors=1)
            bg_colors = get_dominant_colors(background_pixels, n_colors=1)
            
            if text_colors is None or bg_colors is None:
                raise ValueError("Binary threshold method failed")
                
            method = "binary_threshold"
            
        except Exception as e:
            # 모든 방법 실패 시 간단한 통계 사용
            pixels = text_roi.reshape(-1, 3)
            mean_color = np.mean(pixels, axis=0)
            
            # 평균보다 밝은 픽셀과 어두운 픽셀 분리
            bright_mask = np.mean(pixels, axis=1) > np.mean(mean_color)
            dark_mask = ~bright_mask
            
            if np.any(bright_mask) and np.any(dark_mask):
                text_colors = [np.mean(pixels[dark_mask], axis=0)]
                bg_colors = [np.mean(pixels[bright_mask], axis=0)]
            else:
                # 극단적인 경우 기본값 사용
                text_colors = [np.array([0, 0, 0])]
                bg_colors = [np.array([255, 255, 255])]
            
            method = "statistical"
    
    # 결과 반환
    text_color = tuple(round(c / 255, 3) for c in text_colors[0])
    bg_color = tuple(round(c / 255, 3) for c in bg_colors[0])
    
    return {
        "text_color": text_color,
        "background_color": bg_color,
        "confidence_score": calculate_contrast_ratio(text_colors[0], bg_colors[0]),
        "method_used": method
    }

def calculate_contrast_ratio(text_color, bg_color):
    """
    텍스트와 배경색 간의 대비 점수를 계산
    """
    def luminance(color):
        rgb = [c / 255 for c in color]
        rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * rgb[2] + 0.7152 * rgb[1] + 0.0722 * rgb[0]
    
    l1 = luminance(text_color)
    l2 = luminance(bg_color)
    
    ratio = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
    return round(ratio, 2)