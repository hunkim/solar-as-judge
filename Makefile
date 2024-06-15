VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3
STREAMLIT = $(VENV)/bin/streamlit

include .env
export

# Need to use python 3.9 for aws lambda
$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt


test: $(VENV)/bin/activate
	$(PYTHON) test.py

clean:
	rm -rf __pycache__
	rm -rf $(VENV)