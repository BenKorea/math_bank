# 📄 tests/test_env_utils.py

import os
import pytest
from modules.secrets import env_utils

def test_get_secret_field_success(monkeypatch):
    """환경변수가 설정된 경우 정상 반환"""
    monkeypatch.setenv("OPENAI_API_KEY", "testkey123")
    result = env_utils.get_secret_field("ignored", "ignored")
    assert result == "testkey123"

def test_get_secret_field_failure(monkeypatch):
    """환경변수가 없을 경우 예외 발생"""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(KeyError) as exc_info:
        env_utils.get_secret_field("ignored", "ignored")
    assert "OPENAI_API_KEY" in str(exc_info.value)
