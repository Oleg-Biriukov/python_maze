NAME := venv
FILE := main.py
PYTHON := $(NAME)/bin/python
PIP := $(NAME)/bin/pip
VENV := $(NAME)/bin/activate

$(VENV):
	@ python3 -m venv $(NAME)

install: $(VENV)
	@ $(PIP) install -r requirements.txt > /dev/null 2>&1

run: install
	@ $(PYTHON) $(FILE) config.txt

run-pretty: install
	@ $(PYTHON) $(FILE) --pretty config.txt

clean:
	rm -rf *cache*
	rm -rf */*cache*

lint: $(VENV)
	@ $(PYTHON) -m mypy *.py || true
	@ $(PYTHON) -m flake8 *.py Maze*/*.py || true

lint-strict: $(VENV)
	@ $(PYTHON) -m flake8 *.py Maze*/*.py || true
	@ $(PYTHON) -mmypy *.py --strict || true
