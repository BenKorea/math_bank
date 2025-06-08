import re
from pathlib import Path
from logger import get_logger

logger = get_logger(__name__)

def parse_filename(filename: str) -> dict:
    """
    파일명에서 메타데이터 추출 (구조: 책_단원_페이지_유형번호.png)
    예: '중학수학1-상_01_12_B03.png' 또는 '중학수학2-하_03_24_Z7.png'
    """
    try:
        name = filename.rstrip(".png")
        parts = name.split("_")

        if len(parts) != 4:
            logger.warning(f"[1단계 실패] 언더스코어 구분이 4부분이 아님: {filename}")
            return {}

        book, chapter, page, type_number = parts

        # 2단계: 문자+숫자 분리
        type_part = ''.join(filter(str.isalpha, type_number))
        number_part = ''.join(filter(str.isdigit, type_number))

        if not type_part or not number_part:
            logger.warning(f"[2단계 실패] 유형 또는 번호 분리 실패: '{type_number}' in {filename}")
            return {}

        metadata = {
            "book": book,
            "chapter": chapter,
            "page": page,
            "type": type_part,
            "number": number_part
        }
        return metadata

    except Exception as e:
        logger.error(f"[예외 발생] {filename} 처리 중 오류: {e}")
        return {}


def run_parse_all_images(directory: Path = Path("data/raw_images")) -> list[dict]:
    """
    주어진 디렉토리 내 모든 PNG 파일의 파일명을 파싱하여 메타데이터 추출
    """
    if not directory.exists():
        logger.error(f"디렉토리가 존재하지 않습니다: {directory}")
        return []

    logger.info(f"'{directory}' 디렉토리의 PNG 파일 파싱 시작")
    results = []
    total_files = 0
    for file in directory.glob("*.png"):
        total_files += 1
        meta = parse_filename(file.name)
        if meta:
            logger.info(f"파싱 성공: {file.name} → {meta}")
            meta["filename"] = file.name
            results.append(meta)
        else:
            logger.warning(f"파싱 실패: {file.name}")

    logger.info(f"총 {total_files}개 중 {len(results)}개 성공적으로 파싱 완료")
    return results
