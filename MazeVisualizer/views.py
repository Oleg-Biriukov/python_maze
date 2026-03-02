import os
import time
from abc import ABC, abstractmethod
from .umodels import Maze, Pathfinder, FileManager

COLORS = {
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "BLUE": "\033[34m",
    "YELLOW": "\033[33m",
    "PURPLE": "\033[35m",
    "LIGHTBLUE": "\033[94m",
    "WHITE": "\033[97m",
    "RESET": "\033[0m",
    "CYAN": "\033[96m"
}


class MazeRenderer(ABC):
    @abstractmethod
    def render(self, maze: Maze) -> None:
        pass


class PlainRenderer(MazeRenderer):
    def render(self, maze: Maze) -> None:
        for y in range(maze.height):
            top_line = ""
            mid_line = ""

            for x in range(maze.width):
                cell = maze.matrix[y][x]
                top_line += "+"
                top_line += "---" if cell.walls["top"] else "   "
                mid_line += "|" if cell.walls["left"] else " "

                if cell.is_start:
                    mid_line += " S "
                elif cell.is_end:
                    mid_line += " F "
                elif cell.is_path:
                    mid_line += " # "
                elif cell.is_42:
                    mid_line += " @ "
                else:
                    mid_line += "   "

            top_line += "+"
            mid_line += "|" if maze.matrix[y][maze.width - 1].walls["right"] else " "
            print(top_line)
            print(mid_line)

        low_line = ""
        for x in range(maze.width):
            low_line += "+"
            low_line += "---" if maze.matrix[maze.height - 1][x].walls["bottom"] else "   "

        low_line += "+"
        print(low_line)


class PrettyRenderer(MazeRenderer):
    def __init__(self) -> None:
        self.color_palette = [
            COLORS["WHITE"], COLORS["RED"], COLORS["GREEN"],
            COLORS["BLUE"], COLORS["YELLOW"], COLORS["PURPLE"],
            COLORS["LIGHTBLUE"]
        ]
        self.color_index = 0

    def next_color(self) -> None:
        self.color_index = (self.color_index + 1) % len(self.color_palette)

    def _get_corner(self, matrix: list, y: int, x: int, width: int, height: int) -> str:
        up = False
        down = False
        left = False
        right = False

        if y > 0:
            up = matrix[y - 1][x].walls["left"] if x < width else matrix[y - 1][x - 1].walls["right"]
        if y < height:
            down = matrix[y][x].walls["left"] if x < width else matrix[y][x - 1].walls["right"]
        if x > 0:
            left = matrix[y][x - 1].walls["top"] if y < height else matrix[y - 1][x - 1].walls["bottom"]
        if x < width:
            right = matrix[y][x].walls["top"] if y < height else matrix[y - 1][x].walls["bottom"]

        index = (1 if up else 0) + (2 if down else 0) + (4 if right else 0) + (8 if left else 0)
        chars = " ┃┃┃━┗┏┣━┛┓┫━┻┳╋"
        return chars[index]

    def render(self, maze: Maze) -> None:
        color = self.color_palette[self.color_index]
        matrix = maze.matrix
        w = maze.width
        h = maze.height

        for y in range(h):
            top_line = ""
            mid_line = ""

            for x in range(w):
                cell = matrix[y][x]
                top_line += self._get_corner(matrix, y, x, w, h)
                top_line += "━━━" if cell.walls["top"] else "   "
                mid_line += "┃" if cell.walls["left"] else " "

                if cell.is_start:
                    mid_line += " S "
                elif cell.is_end:
                    mid_line += " F "
                elif cell.is_path:
                    mid_line += " # "
                elif cell.is_42:
                    mid_line += f"{COLORS['CYAN']}███{color}"
                else:
                    mid_line += "   "

            top_line += self._get_corner(matrix, y, w, w, h)
            mid_line += "┃" if matrix[y][w - 1].walls["right"] else " "

            print(f"{color}{top_line}{COLORS['RESET']}")
            print(f"{color}{mid_line}{COLORS['RESET']}")

        low_line = ""
        for x in range(w):
            low_line += self._get_corner(matrix, h, x, w, h)
            low_line += "━━━" if matrix[h - 1][x].walls["bottom"] else "   "

        low_line += self._get_corner(matrix, h, w, w, h)
        print(f"{color}{low_line}{COLORS['RESET']}")


class MazeApp:
    def __init__(self, maze: Maze, renderer: MazeRenderer) -> None:
        self.maze = maze
        self.renderer = renderer
        self.pathfinder = Pathfinder()
        self.first_launch = True

    def run(self) -> None:
        os.system("clear")
        self.renderer.render(self.maze)

        while True:
            menu_text = (
                "Choose command:\n"
                "c/C - change the color\n"
                "s/S - show the path\n"
                "h/H - hide the path\n"
                "q/Q - quit the program\n"
                "d/D - delete output file"
            )
            print(menu_text)

            terminal_input = input("Enter: ").lower()

            if terminal_input == "c":
                if isinstance(self.renderer, PrettyRenderer):
                    self.renderer.next_color()
                self._refresh_screen()

            elif terminal_input == "s":
                self.maze.reset_paths()
                final_destination = ""

                for path, direction_path in self.pathfinder.solve(self.maze):
                    os.system("clear")
                    final_destination = direction_path

                    for row in self.maze.matrix:
                        for cell in row:
                            cell.is_path = False

                    for py, px in path:
                        self.maze.matrix[py][px].is_path = True

                    self.renderer.render(self.maze)
                    time.sleep(0.1)

                if self.first_launch:
                    FileManager.save_path(final_destination)
                    self.first_launch = False

            elif terminal_input == "h":
                self.maze.reset_paths()
                self._refresh_screen()

            elif terminal_input == "q":
                os.system("clear")
                break

            elif terminal_input == "rq":
                self.first_launch = True
                pass

            elif terminal_input == "d":
                FileManager.delete()
                self._refresh_screen()

            else:
                self._refresh_screen()

    def _refresh_screen(self) -> None:
        os.system("clear")
        self.renderer.render(self.maze)