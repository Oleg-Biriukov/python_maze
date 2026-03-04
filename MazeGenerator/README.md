# MazeGenerator

A Python package for generating mazes using the backtracking algorithm with optional text embedding support.

## Description

MazeGenerator creates perfect or imperfect mazes using a stack-based backtracking algorithm. It supports embedding text patterns (like "42") within the maze structure, where the text areas remain untouched by the maze generation process.

## Installation

### Requirements

- Python >= 3.10
- pydantic >= 2.0

### Install from source

```bash
pip install .
```

### Install with development dependencies

```bash
pip install ".[dev]"
```

Development dependencies include:
- pytest
- black
- ruff
- mypy

## Usage

```python
from MazeGenerator import MazeGenerator

# Define a text pattern (1 = text cell, 0 = maze cell)
text_pattern = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1]
]

# Create a maze generator instance
maze = MazeGenerator(
    width=20,       # Maze width (1-70)
    height=20,      # Maze height (1-70)
    perfect=True,   # True = perfect maze, False = has loops
    text=text_pattern
)

# Generate the maze
maze.generate_maze()

# Get maze seed as hex string
print(str(maze))
```

### Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `width` | int | 1-70 | Width of the maze |
| `height` | int | 1-70 | Height of the maze |
| `perfect` | bool | - | If `True`, generates a perfect maze (single solution). If `False`, removes ~10% of walls to create loops |
| `text` | List[List[int]] | - | 2D array where `1` represents text cells and `0` represents maze cells |

### Cell Types

- **WALL**: Regular maze cells that participate in maze generation
- **TEXT**: Protected cells that form the embedded text pattern

### Wall Representation

Walls are represented using binary flags:
- `N` (North): `0b0001`
- `E` (East): `0b0010`
- `S` (South): `0b0100`
- `W` (West): `0b1000`
- `CLOSE` (All walls): `0b1111`

## Project Structure

```
MazeGenerator/
├── __init__.py        # Module exports
├── MazeGenerator.py   # Main implementation
├── pyproject.toml     # Package configuration
└── README.md          # This file
```

## Build System

This package uses `setuptools` as the build backend:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

## Development

### Code Formatting

```bash
black MazeGenerator.py
```

### Linting

```bash
ruff check MazeGenerator.py
```

### Type Checking

```bash
mypy MazeGenerator.py
```

### Running Tests

```bash
pytest
```

## Authors

- obirukov
- vlprysia
