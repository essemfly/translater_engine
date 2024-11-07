import fitz  # PyMuPDF

from typing import Tuple


def replace_text_in_box(
    doc: fitz.Document,
    page_number: int,
    box_rect: Tuple[float, float, float, float],
    new_text: str,
    font_size: float = 11,
    font_name: str = "Gulim",
    text_color: Tuple[float, float, float] = (0, 0, 0),
    bg_color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> fitz.Document:
    """PDF 페이지의 특정 영역의 텍스트를 새로운 텍스트로 교체하고 변경된 PDF 반환
    자동 줄바꿈 기능 포함

    Args:
        doc (fitz.Document): PDF 문서 객체
        page_number (int): 페이지 번호 (0부터 시작)
        box_rect (tuple): 박스의 좌표 (x0, y0, x1, y1)
        new_text (str): 새로 입력할 텍스트
        font_size (float): 폰트 크기
        font_name (str): 폰트 이름
        text_color (tuple): 텍스트 색상 RGB 값 (0-1 사이 값)
        bg_color (tuple): 배경색 RGB 값 (0-1 사이 값)

    Returns:
        fitz.Document: 수정된 PDF 문서 객체
    """

    try:
        font_path = "./fonts/NanumGothicCoding.ttf"
        page = doc[page_number]

        # 배경 사각형 그리기
        page.draw_rect(box_rect, color=None, fill=bg_color)

        # 박스의 너비 계산
        box_width = box_rect[2] - box_rect[0]

        # 폰트 객체 생성
        font = fitz.Font(fontfile=font_path)

        # 텍스트를 적절한 길이로 나누기
        words = new_text.split()
        lines = []
        current_line = []
        current_length = 0
        space_width = font.text_length(" ", fontsize=font_size)

        for word in words:
            word_length = font.text_length(word, fontsize=font_size)
            # 현재 줄이 비어있는 경우
            if not current_line:
                current_line.append(word)
                current_length = word_length
            # 현재 줄에 단어를 추가할 수 있는 경우
            elif current_length + space_width + word_length <= box_width:
                current_line.append(word)
                current_length += space_width + word_length
            # 현재 줄이 가득 찬 경우
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_length

        # 마지막 줄 처리
        if current_line:
            lines.append(" ".join(current_line))

        # 줄 간격 계산 (폰트 크기의 1.2배)
        line_spacing = font_size * 1.2

        # 각 줄 삽입
        for i, line in enumerate(lines):
            y_position = box_rect[1] + (i *line_spacing) + font_size  # 아래에서 위로 텍스트 삽입

            # 박스를 벗어나지 않는지 확인
            if y_position - font_size >= box_rect[1]:  # 텍스트가 박스를 벗어나지 않는지 확인
                page.insert_text(
                    point=(box_rect[0], y_position),
                    text=line,
                    fontfile=font_path,
                    fontname=font_name,
                    fontsize=font_size,
                    color=text_color,
                )
            else:
                print(f"경고: 텍스트가 박스를 벗어남 (줄 {i+1})")
                break

        return doc
    except Exception as e:
        print(f"텍스트 교체 중 오류 발생: {e}")
        return None
