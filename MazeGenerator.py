from enum import Enum, IntFlag
from typing import List
from pydantic import BaseModel, Field, model_validator, PrivateAttr
import random as r
# from mlx import Mlx
# from test import render_maze, seed_to_objects_matrix_converter


class TypeCell(Enum):
    WALL = 'WALL'
    TEXT = 'TEXT'


class WallsType(IntFlag):
    W = 0b0001
    S = 0b0010
    N = 0b1000
    E = 0b0100
    CLOSE = 0b1111


class Colors(Enum):
    pass


class Cell(BaseModel):
    tp: TypeCell
    walls: WallsType = WallsType.CLOSE
    visited: bool = False
    color: Colors = None
    is_path: bool = False


class MazeGenerator(BaseModel):
    width: int = Field(ge=1, le=300)
    height: int = Field(ge=1, le=300)
    entry_x: int = Field(ge=0, le=299)
    entry_y: int = Field(ge=0, le=299)
    exit_x: int = Field(ge=0, le=299)
    exit_y: int = Field(ge=0, le=299)
    perfect: bool = True
    text: List[List[int]] = None
    _maze: List[List] = PrivateAttr(default=[[]])

    @model_validator(mode='after')
    def cannot_equel(self):
        if self.entry_x == self.exit_x:
            raise ValueError('Cannot be same')

        if self.entry_y == self.exit_y:
            raise ValueError('Cannot be same')

        if self.text:
            w = len(self.text[0])
            h = len(self.text)
            if w+2 >= self.width or h+2 >= self.height:
                raise ValueError('The maze too small')
        return self

    def _out_range(self, x: int, y: int) -> bool:
        if x > self.width-1 or x < 0 or y > self.height-1 or y < 0:
            return True
        return False

    def _generate_matrix(self):
        for y in range(0, self.height):
            self._maze.append([])
            for x in range(0, self.width):
                self._maze[y].append(Cell(tp=TypeCell.WALL))

        if self.text:
            w = len(self.text[0])
            h = len(self.text)
            t_x = int((self.width - w) / 2)
            t_y = int((self.height - h) / 2)
            for y in range(0, h):
                for x in range(0, w):
                    if self.text[y][x] == 1:
                        self._maze[y+t_y][x+t_x].tp = TypeCell.TEXT

    def __str__(self):
        result = []
        for y in self._maze:
            for x in y:
                if isinstance(x.walls, WallsType):
                    result.append(hex(x.walls.value)[2:].upper())
                else:
                    result.append(hex(x.walls)[2:].upper())
            # result.append('\n')
        return ''.join(result)

    def paste_text(text_png: list[list[int]]):
        pass

    def render_maze(self):
        def get_corner(y, x):
            up = False
            down = False
            left = False
            right = False

            if y > 0:
                if x < self.width:
                    up = bool(self._maze[y - 1][x].walls.value & 0b0001)
                else:
                    up = bool(self._maze[y - 1][x - 1].walls.value & 0b0100)

            if y < self.height:
                if x < self.width:
                    down = bool(self._maze[y][x].walls.value & 0b0001)
                else:
                    down = bool(self._maze[y][x - 1].walls.value & 0b0100)

            if x > 0:
                if y < self.height:
                    left = bool(self._maze[y][x - 1].walls.value & 0b1000)
                else:
                    left = bool(self._maze[y - 1][x - 1].walls.value & 0b0010)

            if x < self.width:
                if y < self.height:
                    right = bool(self._maze[y][x].walls.value & 0b1000)
                else:
                    right = bool(self._maze[y - 1][x].walls.value & 0b0010)

            index = (1 if up else 0) + (2 if down else 0) + (4 if right else 0) + (8 if left else 0)
            chars = " ┃┃┃━┗┏┣━┛┓┫━┻┳╋"
            return chars[index]

        for y in range(self.height):
            top_line = ""
            mid_line = ""

            for x in range(self.width):
                cell = self._maze[y][x]

                top_line += get_corner(y, x)
                top_line += "━━━" if cell.walls.value & 8 else "   "

                mid_line += "┃" if cell.walls.value & 1 else " "
                mid_line += " # " if cell.is_path else "   "

            top_line += get_corner(y, self.width)
            mid_line += "┃" if self._maze[y][self.width - 1].walls.value & 4 else " "

            print(top_line)
            print(mid_line)

        low_line = ""
        for x in range(self.width):
            low_line += get_corner(self.height, x)
            low_line += "━━━" if self._maze[self.height - 1][x].walls.value & 0b0010 else "   "

        low_line += get_corner(self.height, self.width)
        print(low_line)

    def generate_maze(self):
        self._generate_matrix()
        x, y = 0, 0
        oposite = {
            WallsType.E: WallsType.W,
            WallsType.W: WallsType.E,
            WallsType.S: WallsType.N,
            WallsType.N: WallsType.S
        }
        stack = []
        directions = lambda x, y: {  # noqa
                WallsType.N: (x, y-1),
                WallsType.E: (x+1, y),
                WallsType.S: (x, y+1),
                WallsType.W: (x-1, y)}

        def _neigh(x, y) -> dict[WallsType, int]:
            neigh = {}
            drct = directions(x, y)

            for d, c in drct.items():
                x, y = c
                if self._out_range(x, y):
                    continue
                cell = self._maze[y][x]
                if cell.visited is True or cell.tp is TypeCell.TEXT:
                    continue
                else:
                    neigh[d] = c
            return neigh

        def _break_wall(cell: tuple[int], side: WallsType):
            drct = directions(*cell)
            x, y = cell
            nx, ny = drct[side]
            self._maze[y][x].walls &= ~side & 0b1111
            self._maze[ny][nx].walls &= ~oposite[side] & 0b1111

        def _check_space()

        stack.append((x, y))
        self._maze[y][x].visited = True
        while stack:
            x, y = stack[0]
            del stack[0]
            while _neigh(x, y):
                self._maze[y][x].visited = True
                direct, c = r.choice(list(_neigh(x, y).items()))
                _break_wall((x, y), direct)
                stack.append((x, y))
                x, y = c
            self._maze[y][x].visited = True

        if self.perfect is False:
            to_destoy_x = int((self.width * self.height) * 0.15 / self.height)
            if to_destoy_x == 0:
                to_destoy_x = 1
            for y in range(self.height):
                for x in r.choices(list(range(self.width)), k=to_destoy_x):
                    for dir, cor in directions(x, y).items():
                        if self._out_range(*cor):
                            continue
                        posx, poxy = cor
                        n_cell = self._maze[poxy][posx]
                        cell = self._maze[y][x]
                        if (cell.tp is TypeCell.TEXT or
                                n_cell.tp is TypeCell.TEXT):
                            continue
                        _break_wall((x, y), dir)


def main():
    text_png = [[1, 0, 0, 0, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 1],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 1, 1, 1]]

    maze = MazeGenerator(width=50,
                         height=50,
                         entry_x=0,
                         entry_y=0,
                         exit_x=2,
                         exit_y=2,
                         text=text_png,
                         perfect=False)
    print(maze)
    # maze._generate_matrix()
    # for y in maze._maze:
    #     for x in y:
    #         print(x.tp, end=' ')
    #     print()
    maze.generate_maze()
    maze.render_maze()
    print(maze)


if __name__ == '__main__':
    main()
