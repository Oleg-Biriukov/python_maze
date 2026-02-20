from enum import Enum
from typing import List
from pydantic import BaseModel, Field, model_validator, PrivateAttr
import numpy as np
import random as r
from mlx import Mlx
# from test import render_maze, seed_to_objects_matrix_converter


class TypeCell(Enum):
    BORDER = 'BORDER'
    WALL = 'WALL'
    TEXT = 'TEXT'


class WallsType(Enum):
    W = 0b0001
    S = 0b0010
    N = 0b1000
    E = 0b0100
    S_W = 0b0011
    E_W = 0b0101
    E_S = 0b0110
    N_W = 0b1001
    N_S = 0b1010
    N_E = 0b1100
    E_S_W = 0b0111
    N_S_W = 0b1011
    N_E_W = 0b1101
    N_E_S = 0b1110
    OPEN = 0b0000
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

    def model_post_init(self, __content):
        self._maze = []
        for y in range(0, self.height):
            self._maze.append([])
            for x in range(0, self.width):
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
        out_range = lambda x, y: x > self.width-1 or x < 0 or y > self.height-1 or y < 0 # noqa

        def check_sides(x: int, y: int) -> list[WallsType]:
            filtr_list = [w for w in list(WallsType)
                          if w != WallsType.CLOSE]
            if x == 0 and y == 0:  # top left corner
                return [w for w in filtr_list
                        if w.value & 0b1001]

            if x == self.width-1 and y == 0:  # top right corner
                return [w for w in filtr_list
                        if w.value & 0b1100]

            if x == 0 and y == self.height-1:  # bottom left corner
                return [w for w in filtr_list
                        if w.value & 0b0110]

            if x == self.width-1 and y == self.height-1:  # bottom right corner
                return [w for w in filtr_list
                        if w.value & 0b0011]

            if x > 0 and x < self.width-1 and y == 0:  # top border
                return [w for w in filtr_list
                        if w.value & 0b1000]

            if x > 0 and x < self.width-1 and y == self.height-1:  # bottom border
                return [w for w in filtr_list
                        if w.value & 0b0010]

            if y > 0 and y < self.height-1 and x == 0:  # left border
                return [w for w in filtr_list
                        if w.value & 0b0001]

            if y > 0 and y < self.height-1 and x == self.width-1:  # right border
                return [w for w in filtr_list
                        if w.value & 0b0100]
            return filtr_list

        def track_to(x: int, y: int) -> None:
            if out_range(x, y) or self._maze[y][x].visited is True:
                return
            self._maze[y][x].visited = True
            if x == 0 or y == 0 or x == self.width-1 or y == self.height-1:
                self._maze[y][x].tp = TypeCell.BORDER
            self._maze[y][x].walls = r.choice(check_sides(x, y))
            direct = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            r.shuffle(direct)
            for d in direct:
                # print(d)
                x, y = d
                if out_range(x, y):
                    continue
                track_to(x, y)
            return
        track_to(s_x, s_y)


def main():
    maze = MazeGenerator(width=30,
                         height=30,
                         entry_x=0,
                         entry_y=0,
                         exit_x=2,
                         exit_y=2)
    my_seed4 = "B91553955393939391555555553D13AEC3BAC3BC6AAC6C6C55555553C3EAC396AC56857AAB95513953B956D056BC694553853AAC4396AAD2AA953E93A9545396C7AAC53EC3AC3C6C47C52AC69556C3952C53C53AC3C5179393EA93A95396C3C53A97AABA95296AAC52AAAA96C53C3D6AC52AAC696A96C396AAC2A93945693C53AA87947AC556ABAC3EAAEA953A83BAAA83879697956AC3C56C3AA96AAC2AC6AAA96945693A96955386AC3AAD2A97AC6C3AD152C2A96956ABABC6C3EAC54393AC3C783EC6969546A853FC56FFFAEAAD453EC393AD69556A96FD5157FA96C13BA952AC69569556C3FFFAFFFAA93EAC2A96C39693A9793C53FAFD546AC3C3C6AB96A96C6A96C53AFAFFF956BC3C13AAA9683B9469396A92D5529383C3EAAAAAD6AC2D16AC3AAC5156EC6C3C3AAAAC5383C3C7C3AAA97A95539547C6AA853AAC3C5556AAAC16C53AC395556AABC687A955516A83C7956A92C39792AC13A96AD55296EA95693AAE96C3AAC3AC6A92953EA93C693AC6C3C396AABAC396AEC3C3C6C556C6D1547A856AAC3AC3C55478555557913C5396C53AA96C7A95553A9555396A8556C5396AAAD156AD5546AD53C6BAE95517AE92C456D54555554554556C5457C5456E"

    maze.generate_maze()
    # for y in maze._maze:
    #     for x in y:
    #         print(x.tp.value, end=' ')
    #     print()
    maze.render_maze()


if __name__ == '__main__':
    main()
