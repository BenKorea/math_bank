import os
from pathlib import Path
import logging as std_logging
import pytest

from logger import get_logger, setup_default_logging  # ✅ 새 위치로 수정

LOG_FILE_PATH = Path("logs/dev.log")

def reset_logging():
    for handler in std_logging.root.handlers[:]:
        std_logging.root.removeHandler(handler)
    if LOG_FILE_PATH.exists():
        LOG_FILE_PATH.unlink()

def test_setup_default_logging_creates_log_file_and_writes_message():
    reset_logging()
    setup_default_logging()
    logger = std_logging.getLogger("test_logger")
    logger.info("This is a test log message")

    assert LOG_FILE_PATH.exists(), "로그 파일이 생성되지 않았습니다."

    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        assert "This is a test log message" in content

def test_get_logger_returns_configured_logger():
    reset_logging()
    logger = get_logger("my_test_logger")
    logger.warning("Logger test message")

    assert LOG_FILE_PATH.exists(), "로그 파일이 생성되지 않았습니다."

    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Logger test message" in content
