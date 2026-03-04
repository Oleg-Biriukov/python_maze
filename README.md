# A-Maze-ing

*This project has been created as part of the 42 curriculum by vlprysia, obirukov.*

![image of the maze](./images/img.png)

---

## Table of Contents

- [Description](#description)
- [Instructions](#instructions)
- [Configuration File Format](#configuration-file-format)
- [Algorithm](#algorithm)
- [Visual Representation & Interactions](#visual-representation--interactions)
- [Reusable Components](#reusable-components)
- [Resources](#resources)
- [Team & Project Management](#team--project-management)

---

## Description

A-Maze-ing is a procedural maze generator written in Python that creates, displays, and solves mazes. The project parses a configuration file to generate a maze, ensures there is a valid path from the entry to the exit, and visualizes the result interactively in the terminal.

### Goal

The primary goal of this project is to implement a maze generation algorithm from scratch, understand graph traversal techniques, and create an interactive visualization tool for maze exploration and pathfinding.

### Key Features

- Procedural maze generation using the Recursive Backtracker algorithm
- Support for both perfect mazes (single solution) and imperfect mazes (multiple paths)
- Optional text embedding within the maze structure (e.g., "42" pattern)
- Interactive terminal-based visualization with ASCII/Unicode rendering
- Pathfinding from entry to exit with visual path display
- **Bonus:** Animations during maze generation and pathfinding phases
- Multiple color schemes for visualization
- Seed-based regeneration for reproducible mazes

---

## Instructions

### Prerequisites

- Python 3.13 or higher

### Installation & Execution

You can use the provided `Makefile` to manage the project:

| Command | Description |
|---------|-------------|
| `make install` | Install all dependencies |
| `make run` | Run the program with default config |
| `make clean` | Clean cache and temporary files |
| `make build` | Build the reusable pip package (`.whl` / `.tar.gz`) |

### Quick Start

```bash
make run
```

Or execute directly:

```bash
python3 main.py config.txt
```

### Command-Line Options

- `--pretty` — Enable Unicode rendering for enhanced visual output

---

## Configuration File Format

The program relies on a plain text configuration file with a simple `KEY=VALUE` format.

### Structure

- One `KEY=VALUE` pair per line
- Lines starting with `#` are treated as comments and ignored
- Empty lines are allowed

### Example Configuration

```plaintext
# Maze Configuration File
WIDTH=30
HEIGHT=30
ENTRY=0,1
EXIT=29,28
PERFECT=False
OUTPUT_FILE=maze_output.txt
```

### Configuration Keys

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `WIDTH` | Integer (1-70) | Yes | Width of the maze in cells |
| `HEIGHT` | Integer (1-70) | Yes | Height of the maze in cells |
| `ENTRY` | Coordinates `x,y` | Yes | Entry point coordinates (starting position) |
| `EXIT` | Coordinates `x,y` | Yes | Exit point coordinates (goal position) |
| `PERFECT` | Boolean (`True`/`False`) | Yes | `True` = single unique path; `False` = multiple paths with loops |
| `OUTPUT_FILE` | String | Yes | Filename for saving maze data (leave empty to skip saving) |

---

## Algorithm

### Chosen Algorithm: Recursive Backtracker

We chose the **Recursive Backtracker** (also known as Depth-First Search with backtracking) algorithm for maze generation.

### Why This Algorithm?

1. **Simplicity**: It is one of the most intuitive and easy-to-understand maze generation algorithms
2. **Efficiency**: Stack-based implementation avoids recursion depth limits for large mazes
3. **Quality**: Produces mazes with long, winding corridors and a good aesthetic appearance
4. **Perfect Mazes**: Naturally generates perfect mazes where every cell is reachable and there's exactly one path between any two points

### How It Works

1. Start at a random cell and mark it as visited
2. While there are unvisited cells:
   - If the current cell has unvisited neighbors:
     - Push the current cell to the stack
     - Choose a random unvisited neighbor
     - Remove the wall between the current cell and the chosen neighbor
     - Move to the chosen neighbor and mark it as visited
   - Else (no unvisited neighbors):
     - Pop a cell from the stack and backtrack

### Imperfect Maze Generation

When `PERFECT=False`, after generating the base maze, we intentionally remove approximately 10% of random walls to create loops and multiple paths while ensuring no large empty rooms (3x3) are created.

---

## Visual Representation & Interactions

The maze is rendered in the terminal using ASCII characters by default. Unicode rendering can be enabled with the `--pretty` flag for enhanced visuals.

### Interactive Menu

```text
Choose command:
c/C - change the color
s/S - show the path
h/H - hide the path
q/Q - quit the program
r/R - Re-create with new seed
d/D - delete output file
```

---

## Reusable Components

### MazeGenerator Package

The core maze generation logic is encapsulated in a standalone, reusable Python package located in `MazeGenerator/`.

#### Installation

```bash
cd MazeGenerator
pip install .
```

#### Usage

```python
from MazeGenerator import MazeGenerator

# Optional: Define a text pattern to embed (1 = text, 0 = maze)
text_pattern = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1]
]

# Create and generate maze
maze = MazeGenerator(
    width=30,
    height=30,
    perfect=True,
    text=text_pattern
)
maze.generate_maze()

# Get maze as hex seed string
seed = str(maze)
```

#### Package Structure

```
MazeGenerator/
├── __init__.py        # Module exports
├── MazeGenerator.py   # Core implementation
├── pyproject.toml     # Package configuration
└── README.md          # Package documentation
```

See [MazeGenerator/README.md](MazeGenerator/README.md) for detailed package documentation.

---

## Resources

### Documentation & References

- [Maze Generation Algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker Algorithm — Think Labyrinth](https://www.astrolog.org/labyrnth/algrithm.htm)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Rich Library — Terminal Formatting](https://rich.readthedocs.io/)

### AI Usage

AI tools were used in the following aspects of this project:

| Task | AI Tool | Description |
|------|---------|-------------|
| Documentation | GitHub Copilot | Writing README files, docstrings, and code comments |
| Code Review | GitHub Copilot | Reviewing code structure and suggesting improvements |
| Debugging | GitHub Copilot | Identifying and fixing bugs in edge cases |

**Note:** The core algorithms (maze generation, pathfinding) were implemented manually by the team. AI was used as a supportive tool for documentation and code quality improvements.

---

## Team & Project Management

### Team Roles

| Member | Role | Responsibilities |
|--------|------|------------------|
| **vlprysia** | Lead Developer | Maze generation algorithm, configuration parsing, project architecture |
| **obirukov** | Developer / QA | Visualization module, pathfinding, testing, documentation |

### Project Planning

#### Initial Plan

1. **Week 1**: Research algorithms, set up project structure, implement basic maze generation
2. **Week 2**: Add configuration parsing, implement visualization
3. **Week 3**: Implement pathfinding, add interactions, testing
4. **Week 4**: Polish, documentation, bonus features (animations)

#### How It Evolved

- Maze generation took less time than expected due to clear algorithm documentation
- Visualization required more iterations to achieve smooth terminal rendering
- Added text embedding feature as an additional enhancement
- Bonus animations were implemented ahead of schedule

### What Worked Well

- Clear separation between maze generation (`MazeGenerator`) and visualization (`MazeVisualizer`) modules
- Using Pydantic for data validation simplified error handling
- Early decision to make the generator a reusable package
- Regular communication and code reviews between team members

### What Could Be Improved

- Earlier integration testing between modules
- More comprehensive unit tests from the start
- Better documentation during development (rather than at the end)

### Tools Used

| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **GitHub** | Repository hosting, collaboration |
| **VS Code** | Primary IDE |
| **Python 3.13** | Programming language |
| **Pydantic** | Data validation and settings management |
| **Rich** | Terminal formatting and colors |
| **Make** | Build automation |
| **pytest** | Testing framework |
| **black / ruff** | Code formatting and linting |
| **mypy** | Static type checking |
