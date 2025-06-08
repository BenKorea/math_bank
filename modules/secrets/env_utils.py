# modules/secrets/bw_utils.py

import os
from dotenv import load_dotenv
from logger import get_logger

logger = get_logger(__name__)

# .env 파일 로딩
load_dotenv()

def get_secret_field(item_name: str, field_name: str) -> str:
    """
    환경변수(.env)에서 API 키를 가져옵니다.
    item_name과 field_name은 무시되며 OPENAI_API_KEY만 반환합니다.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        logger.info("✅ OPENAI_API_KEY가 성공적으로 로드되었습니다.")
        return api_key
    else:
        logger.error("❌ OPENAI_API_KEY가 환경변수에 없습니다. .env 파일을 확인하세요.")
        raise KeyError("환경변수 'OPENAI_API_KEY'를 찾을 수 없습니다.")
