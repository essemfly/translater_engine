import fitz  # PyMuPDF


def replace_text_in_box(
    page: fitz.Page,
    box_rect: tuple[float, float, float, float],
    new_text: str,
    font_size: float = 11,
    font_name: str = "helv",
    text_color: tuple = (0, 0, 0),
) -> bool:
    """PDF 페이지의 특정 영역의 텍스트를 새로운 텍스트로 교체

    Args:
        page (fitz.Page): PDF 페이지 객체
        box_rect (tuple): 박스의 좌표 (x0, y0, x1, y1)
        new_text (str): 새로 입력할 텍스트
        font_size (float): 폰트 크기
        font_name (str): 폰트 이름
        text_color (tuple): RGB 색상값 (0-1 사이 값)

    Returns:
        bool: 성공 여부
    """
    try:
        # 해당 영역의 기존 내용을 흰색 사각형으로 덮기
        page.draw_rect(box_rect, color=(1, 1, 1), fill=(1, 1, 1))

        # 새로운 텍스트 삽입
        rc = page.insert_text(
            point=(box_rect[0], box_rect[1]),  # 시작 위치
            text=new_text,
            fontname=font_name,
            fontsize=font_size,
            color=text_color,
        )
        return True if rc else False
    except Exception as e:
        print(f"텍스트 교체 중 오류 발생: {e}")
        return False
