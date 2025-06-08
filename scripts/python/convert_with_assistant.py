from pathlib import Path
from modules.assistant.assistant_client import convert_image_to_qmd
from logger import get_logger

log = get_logger(__name__)

if __name__ == "__main__":
    image_path = Path("data/raw_images/중학수학1-상_01_12_B03.png")
    prompt = "이 수학 문제를 Quarto Markdown 형식으로 변환해줘. 해설도 함께 제공해줘."

    result = convert_image_to_qmd(image_path, prompt)

    output_path = Path("data/problems/staged/중학수학1-상_01_12_B03.qmd")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding="utf-8")

    log.info(f"✅ 변환 결과 저장 완료: {output_path}")
