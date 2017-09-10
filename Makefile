export PATH := $(shell pwd)/venv/bin/:$(PATH)
all: venv

venv:
	virtualenv -p python3.6 venv
	pip install -r requirements-dev.txt -r requirements.txt -e .
	pre-commit install --install-hooks

.PHONY: clean
clean:
	rm -rf venv
	git clean -ffdX

.PHONY: test
test: venv
	pre-commit run --all-files
	pytest tests
	pylint alfred_datetime tests
