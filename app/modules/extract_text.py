import io
from google.cloud import vision


def google_detect_text(image_path: str, client: any) -> str:
    """
    Google Vision API를 사용하여 이미지에서 텍스트를 감지.
    Args:
        image_path (str): 텍스트를 감지할 이미지 파일의 경로
    Returns:
        str: 감지된 텍스트
    """
    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f"API Error: {response.error.message}")

    # 첫 번째 항목이 전체 감지 텍스트, 나머지는 부분 텍스트
    full_text = texts[0].description if texts else ""
    return full_text


def pixels_to_font_point(pixels: int, dpi: int = 96) -> float:
    """
    픽셀 단위 높이를 포인트 단위 글자 크기로 변환합니다.

    Args:
        pixels (int): 픽셀 단위 높이
        dpi (int): 화면 해상도 (기본값: 96 DPI)

    Returns:
        float: 포인트 단위 글자 크기
    """
    points = pixels * 72 / dpi
    return points


def estimate_font_size(bounding_box: list, dpi: int = 96) -> float:
    """
    bounding box 높이를 사용하여 텍스트 크기를 포인트 단위로 추정합니다.

    Args:
        bounding_box (list): [좌상단 x, y, 우하단 x, y] 좌표 리스트
        dpi (int): 화면 해상도 (기본값: 96 DPI)

    Returns:
        float: 추정된 글자 크기 (포인트 단위)
    """
    # bounding box 높이 계산
    text_height_pixels = bounding_box[3] - bounding_box[1]

    # 픽셀을 포인트로 변환
    font_size_points = pixels_to_font_point(text_height_pixels, dpi)
    return font_size_points
