import heapq
import os


class Cell:
    def __init__(self, x: int, y: int, hex_val: str) -> None:
        self.x = x
        self.y = y
        val = int(hex_val, 16)
        self.walls = {
            "top": bool(val & 1),
            "right": bool(val & 2),
            "bottom": bool(val & 4),
            "left": bool(val & 8),
        }
        self.is_42 = val == 15
        self.is_start = False
        self.is_end = False
        self.g = float('inf')
        self.h = 0.0
        self.parent = None
        self.is_path = False

    def reset_pathfinding(self) -> None:
        self.g = float('inf')
        self.h = 0.0
        self.parent = None
        self.is_path = False

    @property
    def f(self) -> float:
        return self.g + self.h

    def __lt__(self, other: "Cell") -> bool:
        return self.f < other.f


class Maze:
    def __init__(self, seed: str, width: int, height: int, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.matrix = self._build_matrix(seed)
        self.matrix[self.start_y][self.start_x].is_start = True
        self.matrix[self.start_y][self.start_x].g = 0
        self.matrix[self.end_y][self.end_x].is_end = True

    def _build_matrix(self, seed: str) -> list:
        cells_list = []
        for y in range(self.height):
            row = [Cell(x, y, seed[y * self.width + x]) for x in range(self.width)]
            cells_list.append(row)
        return cells_list

    def reset_paths(self) -> None:
        for row in self.matrix:
            for cell in row:
                cell.reset_pathfinding()
        self.matrix[self.start_y][self.start_x].g = 0


class Pathfinder:
    @staticmethod
    def manhattan_distance(start_x: int, start_y: int, end_x: int, end_y: int) -> int:
        return abs(start_x - end_x) + abs(start_y - end_y)

    @staticmethod
    def trace_path(end_cell: Cell) -> tuple:
        path = []
        direction_string = ""
        moves = {(0, -1): "N", (0, 1): "S", (1, 0): "E", (-1, 0): "W"}
        current = end_cell

        while current is not None:
            path.append(current)
            current = current.parent

        path = path[::-1]
        path_coords = [(node.y, node.x) for node in path]

        for i in range(len(path) - 1):
            dx = path[i + 1].x - path[i].x
            dy = path[i + 1].y - path[i].y
            direction_string += moves.get((dx, dy), "")

        return path_coords, direction_string

    def solve(self, maze: Maze) -> any:
        directions = [("top", 0, -1), ("right", 1, 0), ("bottom", 0, 1), ("left", -1, 0)]
        start_cell = maze.matrix[maze.start_y][maze.start_x]
        open_list = []
        heapq.heappush(open_list, (start_cell.f, start_cell))
        closed_list = set()

        while open_list:
            _, current_cell = heapq.heappop(open_list)

            if (current_cell.y, current_cell.x) in closed_list:
                continue
            closed_list.add((current_cell.y, current_cell.x))

            coords, directions_path = self.trace_path(current_cell)
            yield coords, directions_path

            if current_cell.x == maze.end_x and current_cell.y == maze.end_y:
                return

            for wall_name, dx, dy in directions:
                if not current_cell.walls[wall_name]:
                    nx = current_cell.x + dx
                    ny = current_cell.y + dy

                    if 0 <= nx < maze.width and 0 <= ny < maze.height:
                        neighbor = maze.matrix[ny][nx]
                        if (ny, nx) in closed_list:
                            continue

                        new_g = current_cell.g + 1
                        if new_g < neighbor.g:
                            neighbor.parent = current_cell
                            neighbor.g = new_g
                            neighbor.h = self.manhattan_distance(nx, ny, maze.end_x, maze.end_y)
                            heapq.heappush(open_list, (neighbor.f, neighbor))



class FileManager:
    FILENAME = "../output_maze.txt"

    @classmethod
    def save_initial_data(cls, seed: str, maze: Maze) -> None:
        with open(cls.FILENAME, "w") as file:
            for rows in range(maze.height):
                for letter in range(maze.width):
                    file.write(f"{seed[rows * maze.width + letter].upper()}")
                file.write("\n")
            file.write(f"\n{maze.start_x},{maze.start_y}\n{maze.end_x},{maze.end_y}\n")

    @classmethod
    def save_path(cls, path: str) -> None:
        with open(cls.FILENAME, "a") as file:
            file.write(path)

    @classmethod
    def delete(cls) -> None:
        if os.path.exists(cls.FILENAME):
            os.remove(cls.FILENAME)