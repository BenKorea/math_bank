.PHONY: env help

env:
	@echo "[RUN] Initializing .env from Bitwarden"
	@bash scripts/init_env.sh

help:
	@echo "🛠️  사용 가능한 make 명령:"
	@echo "  make env        - Bitwarden에서 API 키를 가져와 .env 생성"
