.PHONY: run-server migrate check-style

migrate:
	@echo "Applying database migrations..."
	@poetry run alembic upgrade head
	@echo "Migrations applied successfully."

run-server:
	@echo "Starting server..."
	@poetry run python3 run.py

check-style:
	black --check . 
	ruff check .

