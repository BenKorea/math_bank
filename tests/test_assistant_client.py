# ✅ 파일 위치: tests/test_assistant_client.py

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from modules.assistant import assistant_client

@pytest.fixture
def dummy_image_path(tmp_path):
    path = tmp_path / "dummy.png"
    path.write_bytes(b"fake image content")
    return path

@patch("modules.assistant.assistant_client.openai")
def test_get_or_create_assistant_id_creates_new(mock_openai, tmp_path):
    test_file = tmp_path / "assistant_id.txt"
    with patch("modules.assistant.assistant_client.ASSISTANT_ID_PATH", test_file):
        mock_assistant = MagicMock()
        mock_assistant.id = "asst-test123"
        mock_openai.beta.assistants.create.return_value = mock_assistant

        assistant_id = assistant_client.get_or_create_assistant_id()
        assert assistant_id == "asst-test123"
        assert test_file.exists()
        assert test_file.read_text() == "asst-test123"

@patch("modules.assistant.assistant_client.openai")
def test_get_or_create_assistant_id_reads_existing(mock_openai, tmp_path):
    test_file = tmp_path / "assistant_id.txt"
    test_file.write_text("asst-cached123")
    with patch("modules.assistant.assistant_client.ASSISTANT_ID_PATH", test_file):
        assistant_id = assistant_client.get_or_create_assistant_id()
        assert assistant_id == "asst-cached123"
        mock_openai.beta.assistants.create.assert_not_called()

@patch("modules.assistant.assistant_client.openai")
def test_create_thread(mock_openai):
    mock_thread = MagicMock()
    mock_thread.id = "thread-xyz"
    mock_openai.beta.threads.create.return_value = mock_thread

    thread_id = assistant_client.create_thread()
    assert thread_id == "thread-xyz"

@patch("modules.assistant.assistant_client.openai")
def test_add_image_message(mock_openai, dummy_image_path):
    thread_id = "thread-abc"
    prompt = "convert this image"
    assistant_client.add_image_message(thread_id, dummy_image_path, prompt)

    mock_openai.beta.threads.messages.create.assert_called_once()

@patch("modules.assistant.assistant_client.openai")
def test_run_and_get_response_success(mock_openai):
    thread_id = "thread-abc"
    assistant_id = "asst-123"

    mock_run = MagicMock()
    mock_run.id = "run-001"
    mock_openai.beta.threads.runs.create.return_value = mock_run

    mock_openai.beta.threads.runs.retrieve.side_effect = [
        MagicMock(status="in_progress"),
        MagicMock(status="completed")
    ]

    mock_message = MagicMock()
    mock_message.data = [MagicMock(content=[MagicMock(text=MagicMock(value="final result"))])]
    mock_openai.beta.threads.messages.list.return_value = mock_message

    result = assistant_client.run_and_get_response(thread_id, assistant_id, poll_interval=0)
    assert result == "final result"
