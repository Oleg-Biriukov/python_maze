from enum import Enum
from typing import List
from pydantic import BaseModel, Field, model_validator
import numpy as np


class TypeCell(Enum):
    BORDER = 'BORDER'
    CELL = 'CELL'
    TEXT = 'TEXT'


class Colors(Enum):
    pass


class Cell(BaseModel):
    tp: TypeCell
    walls: List[int] = [1, 1, 1, 1]
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

    @model_validator(mode='after')
    def cannot_equel(self):
        if self.entry_x == self.exit_x:
            raise ValueError('Cannot be same')

        if self.entry_y == self.exit_y:
            raise ValueError('Cannot be same')
        return self

    def generate_matrix(self):
        matrix = np.full((self.width, self.height), Cell(tp=TypeCell.CELL))
        matrix[0, :] = Cell(tp=TypeCell.BORDER, visited=True)
        matrix[-1, :] = Cell(tp=TypeCell.BORDER, visited=True)
        matrix[:, 0] = Cell(tp=TypeCell.BORDER, visited=True)
        matrix[:, -1] = Cell(tp=TypeCell.BORDER, visited=True)
        return matrix

    def generate_maze(self):
        def 


def main():
    maze = MazeGenerator(width=10,
                         height=10,
                         entry_x=0,
                         entry_y=0,
                         exit_x=19,
                         exit_y=19)
    m = maze.generate_matrix()
    for x in m:
        for y in x:
            print(y.tp.value, end=' ')
        print()


if __name__ == '__main__':
    main()
