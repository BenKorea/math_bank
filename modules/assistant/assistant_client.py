# modules/assistant/assistant_client.py

import time
from pathlib import Path
import openai
from modules.secrets.env_utils import get_secret_field
from logger import get_logger

# 🔐 OpenAI API 키 설정
openai.api_key = get_secret_field("openai", "OPENAI_API_KEY")
logger = get_logger(__name__)

# 📁 Assistant ID 저장 경로
ASSISTANT_ID_PATH = Path("config/assistant_id.txt")

# 💬 기본 지시사항 (instruction)
DEFAULT_INSTRUCTIONS = """
수학 문제 이미지를 받아서 아래 형식으로 반환:
- 문제는 LaTeX 수식을 포함한 markdown
- 섹션 구분: 문제, answer:, solution:
- 전체를 .qmd 문서 형식으로 구성
"""

def get_or_create_assistant_id() -> str:
    """
    Assistant ID를 config 파일에서 가져오거나 새 Assistant를 생성하여 저장
    """
    if ASSISTANT_ID_PATH.exists():
        assistant_id = ASSISTANT_ID_PATH.read_text().strip()
        logger.info(f"📁 캐시된 Assistant ID 사용: {assistant_id}")
        return assistant_id

    assistant = openai.beta.assistants.create(
        name="MathQMDGenerator",
        instructions=DEFAULT_INSTRUCTIONS.strip(),
        model="gpt-4o"
    )
    assistant_id = assistant.id
    ASSISTANT_ID_PATH.parent.mkdir(parents=True, exist_ok=True)
    ASSISTANT_ID_PATH.write_text(assistant_id)
    logger.info(f"🆕 새 Assistant 생성 및 config/assistant_id.txt에 저장: {assistant_id}")
    return assistant_id

def create_thread() -> str:
    thread = openai.beta.threads.create()
    logger.info(f"🧵 Thread 생성 완료: {thread.id}")
    return thread.id

def add_image_message(thread_id: str, image_path: Path, prompt: str) -> None:
    with open(image_path, "rb") as f:
        logger.info(f"📤 이미지 업로드: {image_path.name}")
        uploaded_file = openai.files.create(file=f, purpose="assistants")
        file_id = uploaded_file.id

    logger.info(f"📩 메시지 전송 중 (file_id: {file_id})")
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt,
        file_ids=[file_id]  # ✅ 수정 포인트
    )


def run_and_get_response(thread_id: str, assistant_id: str, poll_interval=2) -> str:
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    logger.info(f"⏳ Run 시작: {run.id}")

    while True:
        status = openai.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run.id
        ).status
        logger.info(f"⌛ 현재 상태: {status}")
        if status in ["completed", "failed", "cancelled"]:
            break
        time.sleep(poll_interval)

    if status != "completed":
        logger.error(f"❌ Run 실패 또는 취소됨: {status}")
        return ""

    logger.info("✅ Run 완료. 응답 메시지 추출 중...")
    messages = openai.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content[0].text.value

def convert_image_to_qmd(image_path: Path, prompt: str = "이 이미지를 qmd 문서로 변환해줘") -> str:
    assistant_id = get_or_create_assistant_id()
    thread_id = create_thread()
    add_image_message(thread_id, image_path, prompt)
    return run_and_get_response(thread_id, assistant_id)
