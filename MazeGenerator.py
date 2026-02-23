from enum import Enum, IntFlag
from typing import List
from pydantic import BaseModel, Field, model_validator, PrivateAttr
import random as r
# from mlx import Mlx
# from test import render_maze, seed_to_objects_matrix_converter


class TypeCell(Enum):
    BORDER = 'BORDER'
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
    _maze: List[List] = PrivateAttr()

    @model_validator(mode='after')
    def cannot_equel(self):
        if self.entry_x == self.exit_x:
            raise ValueError('Cannot be same')

        if self.entry_y == self.exit_y:
            raise ValueError('Cannot be same')
        return self

    def _out_range(self, x: int, y: int) -> bool:
        if x > self.width-1 or x < 0 or y > self.height-1 or y < 0:
            return True
        return False

    def model_post_init(self, __content):
        self._maze = []
        for y in range(0, self.height):
            self._maze.append([])
            for x in range(0, self.width):
                if x == 0 or y == 0 or x == self.width-1 or y == self.height-1:
                    self._maze[y].append(Cell(tp=TypeCell.BORDER))
                else:
                    self._maze[y].append(Cell(tp=TypeCell.WALL))

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
        s_x, s_y = 0, 0
        times = (self.height) * (self.width)
        oposite = {
            WallsType.E: WallsType.W,
            WallsType.W: WallsType.E,
            WallsType.S: WallsType.N,
            WallsType.N: WallsType.S
        }
        print(times)

        def _check_corners(x: int, y: int) -> dict[WallsType, tuple[int, int]]:
            filtr_list = {
                WallsType.N: (x, y-1),
                WallsType.E: (x+1, y),
                WallsType.S: (x, y+1),
                WallsType.W: (x-1, y)}

            if x == 0 and y == 0:  # top left corner
                del filtr_list[WallsType.N]
                del filtr_list[WallsType.W]
            elif x == self.width-1 and y == 0:  # top right corner
                del filtr_list[WallsType.N]
                del filtr_list[WallsType.E]
            elif x == 0 and y == self.height-1:  # bottom left corner
                del filtr_list[WallsType.S]
                del filtr_list[WallsType.W]
            elif x == self.width-1 and y == self.height-1:  # bottom right corner
                del filtr_list[WallsType.S]
                del filtr_list[WallsType.E]
            elif x > 0 and x < self.width-1 and y == 0:  # top border
                del filtr_list[WallsType.N]
            elif x > 0 and x < self.width-1 and y == self.height-1:  # bottom border
                del filtr_list[WallsType.S]
            elif y > 0 and y < self.height-1 and x == 0:  # left border
                del filtr_list[WallsType.W]
            elif y > 0 and y < self.height-1 and x == self.width-1:  # right border
                del filtr_list[WallsType.E]
            return filtr_list

        def track_to(x: int, y: int, op: int) -> None:
            if (self._out_range(x, y) or
                    self._maze[y][x].visited is True):
                return
            self._maze[y][x].visited = True
            direct = list(_check_corners(x, y).items())
            r.shuffle(direct)
            print(direct)
            times = 0
            for dir, pos in direct:
                times += 1
                if self._out_range(*pos):
                    continue
                if op is not None and times == 1:
                    self._maze[y][x].walls &= ~(dir | op) & 0b1111
                if op is None and times == 1:
                    self._maze[y][x].walls &= ~dir & 0b1111
                track_to(*pos, oposite[dir])
            return
        print(times)
        track_to(s_x, s_y, None)


def main():
    maze = MazeGenerator(width=10,
                         height=10,
                         entry_x=0,
                         entry_y=0,
                         exit_x=2,
                         exit_y=2)
    maze.generate_maze()
    for y in maze._maze:
        for x in y:
            print(bin(x.walls.value), end=' ')
        print()
    maze.render_maze()
    print(maze)


if __name__ == '__main__':
    main()
