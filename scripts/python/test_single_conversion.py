# scripts/python/test_single_conversion.py

from pathlib import Path
from modules.parsing.filename_parser import run_parse_all_images
from modules.assistant.assistant_client import convert_image_to_qmd
from logger import get_logger

log = get_logger(__name__)

def main():
    # 1. 이미지 목록 가져오기
    parsed = run_parse_all_images()
    if not parsed:
        log.error("✅ 변환할 이미지가 없습니다.")
        return

    # 2. 첫 번째 이미지 선택
    first = parsed[0]
    image_path = Path("data/raw_images") / first["filename"]
    log.info(f"🎯 선택된 이미지: {image_path}")

    # 3. Assistant API 호출
    try:
        result = convert_image_to_qmd(image_path)
        if not result:
            log.error("❌ 변환 실패: 응답 없음")
            return
    except Exception as e:
        log.exception(f"❌ 변환 중 예외 발생: {e}")
        return

    # 4. 저장 경로 지정
    output_dir = Path("data/problems/staged")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{image_path.stem}.qmd"

    # 5. 파일로 저장
    output_path.write_text(result, encoding="utf-8")
    log.info(f"📄 변환 결과 저장 완료: {output_path}")

if __name__ == "__main__":
    main()
