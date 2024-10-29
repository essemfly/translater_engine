import os
import pytest
from datetime import datetime
import fitz  # PyMuPDF

from core.modules.load_pdf import load_pdf
from core.modules.translate_text import replace_text_in_box
from core.modules.save_translated_pdf import save_pdf


class TestPDFTextReplacementIntegration:
    @pytest.fixture
    def setup_paths(self):
        """테스트에 필요한 경로들을 설정하는 fixture"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        paths = {
            "input_pdf": os.path.join(base_dir, "sample_files", "1.pdf"),
            "output_dir": os.path.join(base_dir, "sample_outputs"),
            "output_pdf": os.path.join(
                base_dir,
                "sample_outputs",
                f'output_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            ),
        }

        # output 디렉토리가 없으면 생성
        os.makedirs(paths["output_dir"], exist_ok=True)

        return paths

    def test_pdf_text_replacement_integration(self, setup_paths):
        """PDF 텍스트 교체 통합 테스트"""
        paths = setup_paths

        # GIVEN: PDF 파일이 존재하는지 확인
        assert os.path.exists(
            paths["input_pdf"]
        ), f"입력 PDF 파일이 없습니다: {paths['input_pdf']}"

        # WHEN: PDF를 로드하고 텍스트를 교체하고 저장
        # 1. PDF 로드
        pdf_doc = load_pdf(paths["input_pdf"])
        assert pdf_doc is not None, "PDF 로드 실패"

        # 2. 첫 페이지만 처리
        page = pdf_doc[0]

        # 3. 텍스트 교체
        # 예시 좌표값 - 실제 PDF에 맞게 조정 필요
        box_rect = (100, 100, 200, 120)
        test_text = "통합 테스트 텍스트"

        success = replace_text_in_box(
            page=page, box_rect=box_rect, new_text=test_text, font_size=11
        )
        assert success, "텍스트 교체 실패"

        # 4. 수정된 PDF 저장
        save_success = save_pdf(pdf_doc, paths["output_pdf"])
        assert save_success, "PDF 저장 실패"

        # THEN: 결과 확인
        # 1. 출력 파일이 생성되었는지 확인
        assert os.path.exists(
            paths["output_pdf"]
        ), f"출력 PDF 파일이 생성되지 않았습니다: {paths['output_pdf']}"

        # 2. 출력 파일이 읽을 수 있는 PDF인지 확인
        try:
            with fitz.open(paths["output_pdf"]) as doc:
                assert doc.page_count > 0, "PDF 페이지가 없습니다"
        except Exception as e:
            pytest.fail(f"생성된 PDF를 읽는 데 실패했습니다: {e}")

        # 3. 파일 크기 확인 (0 바이트가 아닌지)
        assert (
            os.path.getsize(paths["output_pdf"]) > 0
        ), "생성된 PDF 파일이 비어있습니다"

    def teardown_method(self, method):
        """테스트 후 정리 작업"""
        # 여기서 필요한 경우 테스트 출력 파일을 정리할 수 있습니다
        # 단, 결과 검토를 위해 이 예제에서는 파일을 남겨두겠습니다
        pass
