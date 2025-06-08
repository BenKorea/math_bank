#!/bin/bash
set -euo pipefail

# 터미널 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RESET='\033[0m'

echo -e "${YELLOW}🔐 Bitwarden Vault에서 자격 정보 가져오는 중...${RESET}"

# 1. Bitwarden 세션 열기
export BW_SESSION=$(bw unlock --raw)

# 2. 항목 이름 기반으로 값 가져오기 (이름은 사용자가 지정한 값)
OPENAI_KEY=$(bw get password openai-api-key)
ASSISTANT_ID=$(bw get item openai-assistant-id | jq -r '.login.username')

# 3. .env 파일로 저장
cat <<EOF > .env
OPENAI_API_KEY=$OPENAI_KEY
OPENAI_ASSISTANT_ID=$ASSISTANT_ID
EOF

echo -e "${GREEN}✅ .env 파일 생성 완료:${RESET} $(realpath .env)"
