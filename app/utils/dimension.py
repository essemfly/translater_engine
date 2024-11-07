from typing import List, Tuple

from app.modules.google_document import GoogleDocumentBoundingPoly


def normalize_to_point_coords(
    normalized_vertices: GoogleDocumentBoundingPoly,
    page_width_pixels: float,
    page_height_pixels: float,
) -> List[Tuple[float, float]]:
    """정규화된 좌표를 포인트 좌표로 변환

    Args:
        normalized_vertices (GoogleDocumentBoundingPoly): 정규화된 좌표 리스트
        page_width_pixels (float): 페이지의 너비 (픽셀)
        page_height_pixels (float): 페이지의 높이 (픽셀)

    Returns:
        List[Tuple[float, float]]: 포인트 단위의 좌표 리스트
    """
    point_vertices = []
    for vertex in normalized_vertices.normalizedVerticies:
        # 먼저 정규화된 좌표를 픽셀로 변환
        pixel_x = round(vertex.x * page_width_pixels)
        pixel_y = round(vertex.y * page_height_pixels)

        point_vertices.append((pixel_x, pixel_y))
    return point_vertices


def calculate_rect_from_coords(
    pixel_vertices: List[Tuple[float, float]]
) -> Tuple[float, float, float, float]:
    """픽셀 좌표 리스트에서 (x0, y0, x1, y1) 값을 계산

    Args:
        pixel_vertices (List[Tuple[float, float]]): 픽셀 단위의 좌표 리스트

    Returns:
        Tuple[float, float, float, float]: 계산된 (x0, y0, x1, y1)
    """
    x_values = [coord[0] for coord in pixel_vertices]
    y_values = [coord[1] for coord in pixel_vertices]
    x0, x1 = min(x_values), max(x_values)
    y0, y1 = min(y_values), max(y_values)
    return (x0, y0, x1, y1)


def scale_coords_to_pdf_points(
    coords: Tuple[float, float, float, float],
    source_width: float = 1758.0,  # Google Doc 픽셀 너비
    source_height: float = 2275.0,  # Google Doc 픽셀 높이
    target_width: float = 612.0,  # PDF 포인트 너비
    target_height: float = 792.0,  # PDF 포인트 높이
) -> Tuple[float, float, float, float]:
    """Google Doc 픽셀 좌표를 PDF 포인트 좌표로 변환"""

    # 스케일 비율 계산
    width_scale = target_width / source_width
    height_scale = target_height / source_height

    print("coords", coords)
    return (
        coords[0] * width_scale,
        coords[1] * height_scale,
        coords[2] * width_scale,
        coords[3] * height_scale,
    )


def get_paragraph_text(pdf_metadata, paragraph):
    textPart = paragraph.layout.textAnchor.textSegments[0]
    return pdf_metadata.text[int(textPart.startIndex) : int(textPart.endIndex)]


def get_rect_from_paragraph(pdf_metadata_dimension, pdf_dimension, paragraph):
    normalized_vertices = paragraph.layout.boundingPoly
    # 정규화된 좌표를 픽셀 좌표로 변환 -> 0.1 => 150
    pixel_vertices = normalize_to_point_coords(
        normalized_vertices, pdf_metadata_dimension.width, pdf_metadata_dimension.height
    )
    # 픽셀 좌표 리스트에서 (x0, y0, x1, y1) 값을 계산
    rect_vertices = calculate_rect_from_coords(pixel_vertices)
    # PDF 포인트 좌표로 변환
    scale = pdf_dimension[0] / pdf_metadata_dimension.width
    return [int(coord * scale) for coord in rect_vertices]
