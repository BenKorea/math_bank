# scripts/python/parse_filenames.py

import re
from pathlib import Path
from modules.parsing.filename_parser import parse_filename  # 분리된 로직 사용시
from log_utils.log_utils import get_logger

logger = get_logger("parse_filenames")

RAW_IMAGE_DIR = Path("data/raw_images")

def extract_metadata(filename: str) -> dict:
    """
    파일명에서 메타데이터 추출
    예: '중학수학1-상_01_12_B_03.png'
         => {'book': '중학수학1-상', 'chapter': '01', 'page': '12', 'type': 'B', 'number': '03'}
    """
    pattern = r"(?P<book>.+?)_(?P<chapter>\d{2})_(?P<page>\d{2})_(?P<type>[A-Z])_(?P<number>\d{2})\.png"
    match = re.match(pattern, filename)
    if match:
        return match.groupdict()
    else:
        logger.warning(f"파일명 형식이 올바르지 않음: {filename}")
        return {}

def parse_all_filenames(directory: Path):
    if not directory.exists():
        logger.error(f"디렉토리 없음: {directory}")
        return []

    metadata_list = []
    for file in directory.glob("*.png"):
        metadata = extract_metadata(file.name)
        if metadata:
            metadata["filename"] = file.name
            metadata_list.append(metadata)
            logger.info(f"파싱 성공: {metadata}")
        else:
            logger.warning(f"파싱 실패: {file.name}")
    return metadata_list

if __name__ == "__main__":
    results = parse_all_filenames(RAW_IMAGE_DIR)
    logger.info(f"총 파싱된 파일 수: {len(results)}")
