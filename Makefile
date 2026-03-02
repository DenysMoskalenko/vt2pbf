lint:
	ruff format
	ruff check --fix

lint-no-format:
	ruff check

test:
	pytest

test-coverage:
	pytest --cov=vt2pbf --cov-report=term-missing --cov-report=html --cov-fail-under=90
