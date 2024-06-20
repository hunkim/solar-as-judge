VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3
STREAMLIT = $(VENV)/bin/streamlit
TWINE = $(VENV)/bin/twine

include .env
export

# Need to use python 3.9 for aws lambda
$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt


test: $(VENV)/bin/activate
	$(PYTHON) test.py

up: $(VENV)/bin/activate
	$(TWINE) upload dist/*

clean:
	rm -rf __pycache__
	rm -rf $(VENV)