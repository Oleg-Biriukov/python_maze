from enum import Enum
from typing import Any
from pydantic import BaseModel, Field, model_validator, PrivateAttr
import numpy as np
import random as r
from mlx import Mlx


txtr = {
    0b0000: [
        "   ",
        "   ",
        "   ",
    ],
    0b0001: [  # W
        "   ",
        "┃  ",
        "   ",
    ],
    0b0010: [  # S
        "   ",
        "   ",
        "━━━",
    ],
    0b0011: [  # S + W
        "   ",
        "┃  ",
        "━━━",
    ],
    0b0100: [  # E
        "   ",
        "  ┃",
        "   ",
    ],
    0b0101: [  # E + W
        "   ",
        "┃ ┃",
        "   ",
    ],
    0b0110: [  # E + S
        "   ",
        "  ┃",
        "━━━",
    ],
    0b0111: [  # E + S + W
        "   ",
        "┃ ┃",
        "━━━",
    ],
    0b1000: [  # N
        "━━━",
        "   ",
        "   ",
    ],
    0b1001: [  # N + W
        "━━━",
        "┃  ",
        "   ",
    ],
    0b1010: [  # N + S
        "━━━",
        "   ",
        "━━━",
    ],
    0b1011: [  # N + S + W
        "━━━",
        "┃  ",
        "━━━",
    ],
    0b1100: [  # N + E
        "━━━",
        "  ┃",
        "   ",
    ],
    0b1101: [  # N + E + W
        "━━━",
        "┃ ┃",
        "   ",
    ],
    0b1110: [  # N + E + S
        "━━━",
        "  ┃",
        "━━━",
    ],
    0b1111: [  # N + E + S + W
        "━━━",
        "┃ ┃",
        "━━━",
    ],
}


class TypeCell(Enum):
    BORDER = 'BORDER'
    CELL = 'CELL'
    WALL = 'WALL'
    TEXT = 'TEXT'


class Colors(Enum):
    pass


class Cell(BaseModel):
    tp: TypeCell
    walls: list = txtr[0b1111]
    visited: bool = False
    color: Colors = None


class MazeGenerator(BaseModel):
    width: int = Field(ge=1, le=300)
    height: int = Field(ge=1, le=300)
    entry_x: int = Field(ge=0, le=299)
    entry_y: int = Field(ge=0, le=299)
    exit_x: int = Field(ge=0, le=299)
    exit_y: int = Field(ge=0, le=299)
    perfect: bool = True
    _maze: np.ndarray = PrivateAttr()

    @model_validator(mode='after')
    def cannot_equel(self):
        if self.entry_x == self.exit_x:
            raise ValueError('Cannot be same')

        if self.entry_y == self.exit_y:
            raise ValueError('Cannot be same')
        return self

    def model_post_init(self, __content):
        self._maze = np.full((self.width, self.height), Cell(tp=TypeCell.CELL))
        # self._maze[0, :] = Cell(tp=TypeCell.BORDER, visited=True,
        #                         walls=txtr[0b0010])
        # self._maze[-1, :] = Cell(tp=TypeCell.BORDER, visited=True,
        #                          walls=txtr[0b1000])
        # self._maze[:, 0] = Cell(tp=TypeCell.BORDER, visited=True,
        #                         walls=txtr[0b0001])
        # self._maze[:, -1] = Cell(tp=TypeCell.BORDER, visited=True,
        #                          walls=txtr[0b0001])
        # self._maze[0][0].walls = txtr[0b0110]
        # self._maze[self.height-1][0].walls = txtr[0b0011]

    def __str__(self):
        result = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                for s_wall in range(0, len(self._maze[y][x].walls)):
                    for time in range(0, self.width):
                        result.append(self._maze[y][time].walls[s_wall])
                    result.append('\n')
        return ''.join(result)

    def generate_maze(self):
        x, y = 1, 1

        def track_to(x, y):
            self._maze[x][y].visited = True
            self._maze[x][y].tp = TypeCell.WALL
            self._maze[x][y].walls = r.choice(txtr)
            if self._maze[x+1][y].visited is False:
                return track_to(x+1, y)
            if self._maze[x-1][y].visited is False:
                return track_to(x-1, y)
            if self._maze[x][y+1].visited is False:
                return track_to(x, y+1)
            if self._maze[x][y-1].visited is False:
                return track_to(x, y-1)
        track_to(x, y)


def main():
    maze = MazeGenerator(width=5,
                         height=5,
                         entry_x=0,
                         entry_y=0,
                         exit_x=2,
                         exit_y=2)
    # maze.generate_maze()
    mlx_ptr = m.mlx_init()
    # print(maze)
    # for wall in txtr[0b1111]:
    #     print(wall)
    m.mlx_loop(mlx_ptr)


if __name__ == '__main__':
    main()
