from enum import Enum, IntFlag
from typing import List
from pydantic import BaseModel, Field, model_validator, PrivateAttr
import random as r


class TypeCell(Enum):
    """TO define two types of walls, where first will be
    ourt wall and second one it is '42' label"""
    WALL = 'WALL'
    TEXT = 'TEXT'


class WallsType(IntFlag):
    """Binary representation of walls"""
    W = 0b1000
    S = 0b0100
    E = 0b0010
    N = 0b0001
    CLOSE = 0b1111


class Cell(BaseModel):
    """Cell object"""
    tp: TypeCell
    walls: WallsType = WallsType.CLOSE
    visited: bool = False
    is_path: bool = False


class MazeGenerator(BaseModel):
    """The class aims to cocreate the maze via Backtracking algorithm
    """
    width: int = Field(ge=1, le=70)
    height: int = Field(ge=1, le=70)
    perfect: bool = True
    text: List[List[int]]
    _maze: List[List[Cell]] = PrivateAttr(default=[[]])

    @model_validator(mode='after')
    def cannot_equel(self) -> 'MazeGenerator':
        if self.text:
            w = len(self.text[0])
            h = len(self.text)
            if w+2 >= self.width or h+2 >= self.height:
                raise ValueError('The maze too small')
        return self

    def _out_range(self, x: int, y: int) -> bool:
        """Local func for checking that my algorithm goes
        out from border or not"""
        if x > self.width-1 or x < 0 or y > self.height-1 or y < 0:
            return True
        return False

    def _generate_matrix(self) -> None:
        """generating the matrix with Cell class in each row"""
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

    def __str__(self) -> str:
        """generate the seed for maze"""
        result = []
        for y in self._maze:
            for x in y:
                if isinstance(x.walls, WallsType):
                    result.append(hex(x.walls.value)[2:].upper())
                else:
                    result.append(hex(x.walls)[2:].upper())
        return ''.join(result)

    def generate_maze(self) -> None:
        """Generate maze it self via backtracking via stack(without recursive)
        It is more efficient way to create, because we have no restriction with
        resolution for maze.(Recursive restriction)"""
        self._generate_matrix()
        x, y = 0, 0
        oposite = {
            WallsType.E: WallsType.W,
            WallsType.W: WallsType.E,
            WallsType.S: WallsType.N,
            WallsType.N: WallsType.S
        }
        stack = []

        def _dirct(x: int, y: int) -> dict[WallsType, tuple[int, int]]:
            """Return the with cord for next pos"""
            return {
                WallsType.N: (x, y-1),
                WallsType.E: (x+1, y),
                WallsType.S: (x, y+1),
                WallsType.W: (x-1, y)}

        def _neigh(x: int, y: int) -> dict[WallsType, tuple[int, int]]:
            """checking all avaible spot arount cord"""
            neigh: dict[WallsType, tuple[int, int]] = {}
            drct: dict[WallsType, tuple[int, int]] = _dirct(x, y)

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

        def _break_wall(cell: tuple[int, int], side: WallsType) -> None:
            """break wall between two cells"""
            drct = _dirct(*cell)
            x, y = cell
            nx, ny = drct[side]
            self._maze[y][x].walls &= ~side & 0b1111
            self._maze[ny][nx].walls &= ~oposite[side] & 0b1111

        def _check_emptiness(x: int, y: int) -> bool:
            """checking empty 3x3 room"""
            def _check_room(x: int, y: int) -> bool:
                for dy in [y+0, y+1, y+2]:
                    if self._maze[dy][x].walls & WallsType.E:
                        return False
                    if self._maze[dy][x+1].walls & WallsType.E:
                        return False
                for dx in [x+0, x+1, x+2]:
                    if self._maze[y][dx].walls & WallsType.S:
                        return False
                    if self._maze[y+1][dx].walls & WallsType.S:
                        return False
                return True

            for dx in [0, 1, 2]:
                for dy in [0, 1, 2]:
                    sx = x - dx
                    sy = y - dy
                    if sx+2 < self.width and sy+2 < self.height and \
                            sx > 0 and sy > 0:
                        if _check_room(sx, sy):
                            return True
            return False

        def _undo_wall(cell: tuple[int, int], side: WallsType) -> None:
            """create the walls between two cells"""
            drct = _dirct(*cell)
            x, y = cell
            nx, ny = drct[side]
            self._maze[y][x].walls |= side
            self._maze[ny][nx].walls |= oposite[side]

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
            to_destoy_x = int((self.width * self.height) * 0.1 / self.height)
            if to_destoy_x == 0:
                to_destoy_x = 5
            for y in range(self.height):
                for x in r.choices(list(range(self.width)), k=to_destoy_x):
                    for dir, cor in _dirct(x, y).items():
                        if self._out_range(*cor):
                            continue
                        posx, poxy = cor
                        n_cell = self._maze[poxy][posx]
                        cell = self._maze[y][x]
                        if (cell.tp is TypeCell.TEXT or
                                n_cell.tp is TypeCell.TEXT):
                            continue
                        _break_wall((x, y), dir)
                        if _check_emptiness(x, y):
                            _undo_wall((x, y), dir)
                        break
