export PATH := $(shell pwd)/venv2/bin/:$(PATH)
export VERSION := $(shell python2.7 setup.py --version)
all: venv

venv:
	virtualenv -p python2.7 venv
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

vendor:
	virtualenv -p python2.7 vendor_venv
	vendor_venv/bin/pip install --prefix vendor -r requirements.txt
	rm -r vendor_venv

.PHONY: datetime-$(VERSION).alfred3workflow
datetime-$(VERSION).alfred3workflow: vendor
	zip -r datetime-$(VERSION).alfred3workflow info.plist icon.png alfred_datetime vendor
