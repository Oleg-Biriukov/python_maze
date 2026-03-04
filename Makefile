NAME := .venv
FILE := main.py
PYTHON := $(NAME)/bin/python
PIP := $(NAME)/bin/pip
VENV := $(NAME)/bin/activate

$(VENV):
	@ python3 -m venv $(NAME)

install: $(VENV)
	@ $(PYTHON) -m pip install -r requirements.txt > /dev/null 2>&1

run: install
	@ $(PYTHON) $(FILE) config.txt

run-pretty: install
	@ $(PYTHON) $(FILE) --pretty config.txt

clean:
	rm -rf $(NAME)
	rm -rf *cache* .mypy*
	rm -rf */*cache* */.mypy*

lint: $(VENV)
	@ $(PYTHON) -m mypy *.py || true
	@ $(PYTHON) -m flake8 *.py Maze*/*.py || true

lint-strict: $(VENV)
	@ $(PYTHON) -m flake8 *.py Maze*/*.py || true
	@ $(PYTHON) -m mypy *.py --strict || true

debug:
	$(PYTHON)  -m pdb main.py

build:
	$(PYTHON) -m build -q -s MazeGenerator --wheel