# tests/test_assistant_client.py

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from modules.assistant import assistant_client

def test_get_or_create_assistant_id(monkeypatch, tmp_path):
    dummy_id = "asst_dummy123"
    id_file = tmp_path / "assistant_id.txt"

    # 존재하는 경우
    id_file.write_text(dummy_id)
    monkeypatch.setattr(assistant_client, "ASSISTANT_ID_PATH", id_file)
    assert assistant_client.get_or_create_assistant_id() == dummy_id

    # 생성되는 경우 (mock openai)
    monkeypatch.setattr(assistant_client, "ASSISTANT_ID_PATH", tmp_path / "new_id.txt")

    dummy_assistant = MagicMock()
    dummy_assistant.id = "asst_mocked"
    with patch("openai.beta.assistants.create", return_value=dummy_assistant):
        new_id = assistant_client.get_or_create_assistant_id()
        assert new_id == "asst_mocked"
        assert (tmp_path / "new_id.txt").exists()

def test_create_thread():
    with patch("openai.beta.threads.create") as mock_create:
        mock_create.return_value.id = "thread_123"
        result = assistant_client.create_thread()
        assert result == "thread_123"

def test_add_image_message(tmp_path):
    dummy_file = tmp_path / "image.png"
    dummy_file.write_bytes(b"fake image content")

    with patch("openai.files.create") as mock_upload, \
         patch("openai.beta.threads.messages.create") as mock_message:
        mock_upload.return_value.id = "file_dummy"
        assistant_client.add_image_message("thread_id", dummy_file, "prompt")
        mock_upload.assert_called_once()
        mock_message.assert_called_once()

def test_run_and_get_response():
    with patch("openai.beta.threads.runs.create") as mock_run_create, \
         patch("openai.beta.threads.runs.retrieve") as mock_retrieve, \
         patch("openai.beta.threads.messages.list") as mock_list:

        mock_run_create.return_value.id = "run_1"
        mock_retrieve.return_value.status = "completed"

        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text=MagicMock(value="결과 텍스트"))]
        mock_list.return_value.data = [mock_msg]

        result = assistant_client.run_and_get_response("thread", "assistant")
        assert result == "결과 텍스트"

def test_convert_image_to_qmd(monkeypatch):
    with patch("modules.assistant.assistant_client.get_or_create_assistant_id", return_value="aid"), \
         patch("modules.assistant.assistant_client.create_thread", return_value="tid"), \
         patch("modules.assistant.assistant_client.add_image_message"), \
         patch("modules.assistant.assistant_client.run_and_get_response", return_value="converted.qmd"):

        result = assistant_client.convert_image_to_qmd(Path("dummy.png"))
        assert result == "converted.qmd"
