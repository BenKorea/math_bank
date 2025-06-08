from logger import get_logger
from modules.parsing.filename_parser import run_parse_all_images

log = get_logger(__name__)

def main():
    log.info("프로젝트 시작")
    results = run_parse_all_images()
    log.info(f"파싱된 문제 수: {len(results)}")

if __name__ == "__main__":
    main()
