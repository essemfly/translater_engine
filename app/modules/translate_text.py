import fitz  # PyMuPDF

from typing import List, Tuple


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
        page = doc[page_number - 1]

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
            y_position = (
                box_rect[1] + (i * line_spacing) + font_size
            )  # 아래에서 위로 텍스트 삽입

            # 박스를 벗어나지 않는지 확인
            if (
                y_position - font_size >= box_rect[1]
            ):  # 텍스트가 박스를 벗어나지 않는지 확인
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


def replace_text_in_box_with_align_old(
    doc: fitz.Document,
    page_number: int,
    box_rect: Tuple[float, float, float, float],
    new_text: str,
    base_font_size: float = 15,
    font_name: str = "Gulim",
    text_color: Tuple[float, float, float] = (0, 0, 0),
    bg_color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    align: str = "left",  # "left", "center", "right" 중 선택
) -> fitz.Document:
    """PDF 페이지의 특정 영역의 텍스트를 새로운 텍스트로 교체하고 변경된 PDF 반환
    텍스트 크기를 자동으로 조절하여 박스에 맞춤, 텍스트 정렬 지원

    Args:
        doc (fitz.Document): PDF 문서 객체
        page_number (int): 페이지 번호 (0부터 시작)
        box_rect (tuple): 박스의 좌표 (x0, y0, x1, y1)
        new_text (str): 새로 입력할 텍스트
        font_name (str): 폰트 이름
        text_color (tuple): 텍스트 색상 RGB 값 (0-1 사이 값)
        bg_color (tuple): 배경색 RGB 값 (0-1 사이 값)
        align (str): 텍스트 정렬 방식 ("left", "center", "right")

    Returns:
        fitz.Document: 수정된 PDF 문서 객체
    """

    min_font_size: float = 8
    max_font_size: float = 200

    try:
        if align not in ["left", "center", "right"]:
            raise ValueError(
                "align 매개변수는 'left', 'center', 'right' 중 하나여야 합니다."
            )

        font_path = "./fonts/NanumGothicCoding.ttf"
        page = doc[page_number - 1]

        # 박스 크기 계산
        box_width = box_rect[2] - box_rect[0]
        box_height = box_rect[3] - box_rect[1]

        def try_text_fitting(font_size: float) -> Tuple[bool, List[Tuple[str, float]]]:
            print("try_text_fitting", font_size)
            """주어진 폰트 크기로 텍스트가 박스에 맞는지 확인하고 라인과 길이 목록 반환"""
            font = fitz.Font(fontfile=font_path)
            words = new_text.split()
            lines = []
            current_line = []
            current_length = 0
            space_width = font.text_length(" ", fontsize=font_size)

            for word in words:
                word_length = font.text_length(word, fontsize=font_size)
                if not current_line:
                    current_line.append(word)
                    current_length = word_length
                elif current_length + space_width + word_length <= box_width:
                    current_line.append(word)
                    current_length += space_width + word_length
                else:
                    line_text = " ".join(current_line)
                    line_width = font.text_length(line_text, fontsize=font_size)
                    lines.append((line_text, line_width))
                    current_line = [word]
                    current_length = word_length

            if current_line:
                line_text = " ".join(current_line)
                line_width = font.text_length(line_text, fontsize=font_size)
                lines.append((line_text, line_width))

            # 전체 텍스트 높이 계산 (줄 간격은 폰트 크기의 1.2배)
            total_height = len(lines) * (font_size * 1.2)

            # 박스에 맞는지 확인
            fits = total_height <= box_height
            return fits, lines

        # 이진 탐색으로 적절한 폰트 크기 찾기
        left = min_font_size
        right = max_font_size
        optimal_font_size = min_font_size
        optimal_lines = []

        while left <= right:

            mid = (left + right) / 2

            fits, lines = try_text_fitting(mid)
            if fits:
                optimal_font_size = mid
                optimal_lines = lines
                left = mid + 0.5
            else:
                right = mid - 0.5

        # 배경 사각형 그리기
        page.draw_rect(box_rect, color=None, fill=bg_color)

        # 텍스트 정렬 및 삽입
        line_spacing = optimal_font_size * 1.2

        for i, (line, line_width) in enumerate(optimal_lines):
            # 정렬에 따른 x 좌표 계산
            if align == "left":
                x_position = box_rect[0]
            elif align == "center":
                x_position = box_rect[0] + (box_width - line_width) / 2
            else:  # right
                x_position = box_rect[0] + (box_width - line_width)

            y_position = box_rect[1] + (i * line_spacing) + optimal_font_size

            page.insert_text(
                point=(x_position, y_position),
                text=line,
                fontfile=font_path,
                fontname=font_name,
                fontsize=optimal_font_size,
                color=text_color,
            )

        return doc
    except Exception as e:
        print(f"텍스트 교체 중 오류 발생: {e}")
        return None


def replace_text_in_box_with_align(
    doc: fitz.Document,
    page_number: int,
    box_rect: Tuple[float, float, float, float],
    new_text: str,
    base_font_size: float = 15,
    font_name: str = "Gulim",
    text_color: Tuple[float, float, float] = (0, 0, 0),
    bg_color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    align: str = "left",
) -> fitz.Document:
    """PDF 페이지의 특정 영역의 텍스트를 새로운 텍스트로 교체하고 변경된 PDF 반환
    텍스트 크기를 자동으로 조절하여 박스에 맞춤, 텍스트 정렬 지원
    """
    MIN_FONT_SIZE = 4  # 최소 폰트 크기를 더 작게 설정
    MAX_FONT_SIZE = 200
    EPSILON = 0.1  # 이진 탐색 종료 조건을 위한 임계값

    try:
        if align not in ["left", "center", "right"]:
            raise ValueError(
                "align 매개변수는 'left', 'center', 'right' 중 하나여야 합니다."
            )

        font_path = "./fonts/NanumGothicCoding.ttf"
        page = doc[page_number - 1]

        box_width = box_rect[2] - box_rect[0]
        box_height = box_rect[3] - box_rect[1]

        def try_text_fitting(font_size: float) -> Tuple[bool, List[Tuple[str, float]]]:
            """주어진 폰트 크기로 텍스트가 박스에 맞는지 확인"""
            if font_size < MIN_FONT_SIZE:
                return False, []

            font = fitz.Font(fontfile=font_path)
            words = new_text.split()
            lines = []
            current_line = []
            current_length = 0
            space_width = font.text_length(" ", fontsize=font_size)

            # 한 글자씩 처리하도록 수정
            if box_width < font.text_length("가", fontsize=font_size):
                return False, []

            for word in words:
                # 단어가 너무 길면 글자 단위로 분리
                if font.text_length(word, fontsize=font_size) > box_width:
                    for char in word:
                        char_length = font.text_length(char, fontsize=font_size)
                        if not current_line or current_length + char_length > box_width:
                            if current_line:
                                line_text = "".join(current_line)
                                lines.append((line_text, current_length))
                                current_line = []
                                current_length = 0
                            current_line.append(char)
                            current_length = char_length
                        else:
                            current_line.append(char)
                            current_length += char_length
                else:
                    word_length = font.text_length(word, fontsize=font_size)
                    if not current_line:
                        current_line.append(word)
                        current_length = word_length
                    elif current_length + space_width + word_length <= box_width:
                        current_line.append(word)
                        current_length += space_width + word_length
                    else:
                        line_text = " ".join(current_line)
                        lines.append((line_text, current_length))
                        current_line = [word]
                        current_length = word_length

            if current_line:
                line_text = " ".join(current_line)
                lines.append((line_text, current_length))

            total_height = len(lines) * (font_size * 1.2)
            return total_height <= box_height, lines

        # 이진 탐색으로 적절한 폰트 크기 찾기
        left = MIN_FONT_SIZE
        right = MAX_FONT_SIZE
        optimal_font_size = MIN_FONT_SIZE
        optimal_lines = []

        while (right - left) > EPSILON:
            mid = (left + right) / 2
            fits, lines = try_text_fitting(mid)

            if fits:
                optimal_font_size = mid
                optimal_lines = lines
                left = mid
            else:
                right = mid

        if not optimal_lines:  # 적절한 크기를 찾지 못한 경우
            raise ValueError("텍스트를 박스에 맞출 수 없습니다.")

        # 배경 사각형 그리기
        page.draw_rect(box_rect, color=None, fill=bg_color)

        # 텍스트 정렬 및 삽입
        line_spacing = optimal_font_size * 1.2
        font = fitz.Font(fontfile=font_path)

        for i, (line, line_width) in enumerate(optimal_lines):
            # 실제 라인 너비 재계산
            actual_width = font.text_length(line, fontsize=optimal_font_size)

            if align == "left":
                x_position = box_rect[0]
            elif align == "center":
                x_position = box_rect[0] + (box_width - actual_width) / 2
            else:  # right
                x_position = box_rect[0] + (box_width - actual_width)

            y_position = box_rect[1] + (i * line_spacing) + optimal_font_size

            page.insert_text(
                point=(x_position, y_position),
                text=line,
                fontfile=font_path,
                fontname=font_name,
                fontsize=optimal_font_size,
                color=text_color,
            )

        return doc

    except Exception as e:
        print(f"텍스트 교체 중 오류 발생: {e}")
        return None


def replace_text_in_box_single_line(
    doc: fitz.Document,
    page_number: int,
    box_rect: Tuple[float, float, float, float],
    new_text: str,
    font_size: float = 11,
    font_name: str = "Gulim",
    text_color: Tuple[float, float, float] = (0, 0, 0),
    bg_color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    align: str = "left",
) -> fitz.Document:
    """PDF 페이지의 특정 영역의 텍스트를 한 줄로 새로운 텍스트로 교체하고 변경된 PDF 반환
    텍스트 크기를 자동으로 조절하여 박스에 맞춤, 가로 정렬 및 세로 중앙 정렬 지원
    """
    MIN_FONT_SIZE = 0
    MAX_FONT_SIZE = 200
    EPSILON = 0.1

    try:
        if align not in ["left", "center", "right"]:
            raise ValueError(
                "align 매개변수는 'left', 'center', 'right' 중 하나여야 합니다."
            )

        font_path = "./fonts/NanumGothicCoding.ttf"
        page = doc[page_number - 1]

        box_width = box_rect[2] - box_rect[0]
        box_height = box_rect[3] - box_rect[1]

        def try_text_fitting(font_size: float) -> bool:
            """주어진 폰트 크기로 텍스트가 박스에 맞는지 확인"""
            if font_size < MIN_FONT_SIZE:
                return False

            font = fitz.Font(fontfile=font_path)
            text_width = font.text_length(new_text, fontsize=font_size)
            text_height = font_size

            return text_width <= box_width and text_height <= box_height

        # 이진 탐색으로 적절한 폰트 크기 찾기
        left = MIN_FONT_SIZE
        right = MAX_FONT_SIZE
        optimal_font_size = MIN_FONT_SIZE

        while (right - left) > EPSILON:
            mid = (left + right) / 2
            if try_text_fitting(mid):
                optimal_font_size = mid
                left = mid
            else:
                right = mid

        if not try_text_fitting(optimal_font_size):
            raise ValueError("텍스트를 박스에 맞출 수 없습니다.")

        # 배경 사각형 그리기
        page.draw_rect(box_rect, color=None, fill=bg_color)

        # 텍스트 정렬 및 삽입
        font = fitz.Font(fontfile=font_path)
        text_width = font.text_length(new_text, fontsize=optimal_font_size)

        # 가로 정렬 위치 계산
        if align == "left":
            x_position = box_rect[0]
        elif align == "center":
            x_position = box_rect[0] + (box_width - text_width) / 2
        else:  # right
            x_position = box_rect[0] + (box_width - text_width)

        # 세로 중앙 정렬 위치 계산
        y_position = box_rect[1] + (box_height + optimal_font_size) / 2

        page.insert_text(
            point=(x_position, y_position),
            text=new_text,
            fontfile=font_path,
            fontname=font_name,
            fontsize=optimal_font_size,
            color=text_color,
        )

        return doc

    except Exception as e:
        print(f"텍스트 교체 중 오류 발생: {e}")
        return None
