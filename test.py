import os
import heapq
import time
import argparse

# ━ ┃ ┏ ┓ ┗  ┛ ┣  ┫  ┳ ╋  ┻

RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
PURPLE = "\033[35m"
LIGHTBLUE = "\033[94m"
WHITE = "\033[97m"
RESET = "\033[0m"
CYAN = "\033[96m"


class Cell:
    def __init__(self, x: int, y: int, hex_val: str):
        self.x = x
        self.y = y
        val = int(hex_val, 16)
        self.walls = {
            "top": bool(val & 1),
            "right": bool(val & 2),
            "bottom": bool(val & 4),
            "left": bool(val & 8),
        }
        self.g = float('inf')
        self.h = 0
        self.parent = None
        self.is_path = False
        self.is_end = False
        self.is_start = False
        self.is_42 = val == 15


    def __lt__(self, other):
        return self.f < other.f

    @property
    def f(self):
        return self.g + self.h

def seed_to_objects_matrix_converter(seed: str, width: int, height: int):
    cells_list = []
    for y in range(height):
        row = []
        for x in range(width):
            cell = Cell(x, y, seed[y * width + x])
            row.append(cell)
        cells_list.append(row)
    return cells_list


def get_corner(matrix, y, x, width, height):
    up = False
    down = False
    left = False
    right = False

    if y > 0:
        if x < width:
            up = matrix[y - 1][x].walls["left"]
        else:
            up = matrix[y - 1][x - 1].walls["right"]

    if y < height:
        if x < width:
            down = matrix[y][x].walls["left"]
        else:
            down = matrix[y][x - 1].walls["right"]

    if x > 0:
        if y < height:
            left = matrix[y][x - 1].walls["top"]
        else:
            left = matrix[y - 1][x - 1].walls["bottom"]

    if x < width:
        if y < height:
            right = matrix[y][x].walls["top"]
        else:
            right = matrix[y - 1][x].walls["bottom"]

    index = (1 if up else 0) + (2 if down else 0) + (4 if right else 0) + (8 if left else 0)
    chars = " ┃┃┃━┗┏┣━┛┓┫━┻┳╋"
    return chars[index]


def render_maze(matrix, width, height, color_id:int):
    colors = [WHITE, RED, GREEN, BLUE, YELLOW, PURPLE, LIGHTBLUE]

    color_id = color_id % len(colors)
    for y in range(height):
        top_line = ""
        mid_line = ""

        for x in range(width):
            cell = matrix[y][x]

            top_line += get_corner(matrix, y, x, width, height)
            top_line += "━━━" if cell.walls["top"] else "   "

            mid_line += "┃" if cell.walls["left"] else " "
            if cell.is_start:
                mid_line += " S "
            elif cell.is_end:
                mid_line += " F "
            elif cell.is_path:
                mid_line += " # "
            elif cell.is_42:
                mid_line += f"{CYAN}███{colors[color_id]}"
            else:
                mid_line += "   "


        top_line += get_corner(matrix, y, width, width, height)
        mid_line += "┃" if matrix[y][width - 1].walls["right"] else " "

        print(f"{colors[color_id]}{top_line}{RESET}")
        #time.sleep(0.2)
        print(f"{colors[color_id]}{mid_line}{RESET}")
        #time.sleep(0.2)

    low_line = ""
    for x in range(width):
        low_line += get_corner(matrix, height, x, width, height)
        low_line += "━━━" if matrix[height - 1][x].walls["bottom"] else "   "

    low_line += get_corner(matrix, height, width, width, height)
    print(f"{colors[color_id]}{low_line}{RESET}")


def render_maze_plain(matrix, width, height):
    for y in range(height):
        top_line = ""
        mid_line = ""

        for x in range(width):
            cell = matrix[y][x]

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
        mid_line += "|" if matrix[y][width - 1].walls["right"] else " "

        print(top_line)
        print(mid_line)

    low_line = ""
    for x in range(width):
        low_line += "+"
        low_line += "---" if matrix[height - 1][x].walls["bottom"] else "   "

    low_line += "+"
    print(low_line)



def manhattan_distance(start_x,start_y, end_x, end_y):
    return abs(start_x - end_x) + abs(start_y - end_y)

def trace_path(end_cell):
    path = []
    direction_string = ""
    moves = {
        (0, -1): "N",
        (0, 1): "S",
        (1, 0): "E",
        (-1, 0): "W"
    }
    current =  end_cell

    while current is not None:
        path.append(current)
        current = current.parent

    path = path[::-1]

    path_coords = [(node.y, node.x) for node in path]

    for i in range(len(path) -1):
        curr = path[i]
        nxt = path[i+1]

        dx = nxt.x - curr.x
        dy = nxt.y - curr.y

        direction_string += moves.get((dx, dy), "")

    return path_coords, direction_string

def solve_maze(matrix, width, height, start_x, start_y, end_x, end_y):
    directions = [
        ("top", 0, -1),
        ("right", 1, 0),
        ("bottom", 0, 1),
        ("left", -1, 0)
    ]


    start_cell = matrix[start_y][start_x]

    open_list = []
    heapq.heappush(open_list,(start_cell.f, start_cell))

    closed_list = set()

    while open_list:
        current_f, current_cell = heapq.heappop(open_list)

        if(current_cell.y, current_cell.x) in closed_list:
            continue
        closed_list.add((current_cell.y, current_cell.x))

        coords, directions_path = trace_path(current_cell)

        yield coords, directions_path

        if current_cell.x == end_x and current_cell.y == end_y:
            return

        for wall_name, dx, dy in directions:
            if not current_cell.walls[wall_name]:
                nx,ny = current_cell.x + dx, current_cell.y + dy

                if 0 <= nx < width and 0 <= ny < height:
                    neighbor = matrix[ny][nx]

                    if (ny,nx) in closed_list:
                        continue


                    new_g = current_cell.g + 1
                    if new_g < neighbor.g:
                        neighbor.parent = current_cell
                        neighbor.g = new_g
                        neighbor.h = manhattan_distance(nx, ny, end_x, end_y)
                        heapq.heappush(open_list, (neighbor.f, neighbor))



def write_seed_to_file(seed:str, width:int, height:int):
    with open("output_maze.txt", "w") as file:
        for rows in range(height):
            for letter in range(width):
                file.write(f"{seed[rows*width+letter].upper()}")
            file.write("\n")
        file.write("\n")


def write_coordinates_to_file(sx:int, sy:int, ex:int, ey:int):
    try:
        with open("output_maze.txt", "a") as file:
            file.write(f"{sx},{sy}\n{ex},{ey}\n")
    except FileNotFoundError:
        print("File not exist")


def write_path_to_file(path:str):
    with open("output_maze.txt", "a") as file:
        file.write(path)

def maze_run(seed:str, width:int, height:int, start_x:int, start_y:int, end_x:int, end_y:int, args):
    os.system("clear")
    matrix = seed_to_objects_matrix_converter(seed, width, height)

    matrix[start_y][start_x].g = 0
    matrix[start_y][start_x].is_start = True
    matrix[end_y][end_x].is_end = True
    i = 0
    if args.pretty:
        render_maze(matrix, width, height, i)
    else:
        render_maze_plain(matrix, width, height)
    first_launch = True

    while 1:
        print("Choose command:\nc/C - change the color\ns/S - show the path\nh/H - hide the path\nq/Q - quit the program\nd/D - delete output file")
        terminal_input = input("Enter: ")
        if terminal_input == "c" or terminal_input == "C":
            os.system("clear")
            i += 1
            render_maze(matrix, width, height, i)

        elif terminal_input == "s" or terminal_input == "S":
            for row in matrix:
                for cell in row:
                    cell.g = float('inf')
                    cell.h = 0
                    cell.parent = None
                    cell.is_path = False

            matrix[start_y][start_x].g = 0
            final_destination = ""
            for path_data in solve_maze(matrix, width, height, start_x, start_y, end_x, end_y):
                os.system("clear")

                path, direction_path = path_data
                final_destination = direction_path

                for row in matrix:
                    for cell in row:
                        cell.is_path = False

                for py, px in path:
                    matrix[py][px].is_path = True

                render_maze(matrix, width, height, i)
                time.sleep(0.1)
            if first_launch:
                write_path_to_file(final_destination)
                first_launch = False

        elif terminal_input == "h" or terminal_input == "H":
            os.system("clear")
            for row in matrix:
                for cell in row:
                    cell.is_path = False
            render_maze(matrix, width, height, i)

        elif terminal_input == "q" or terminal_input == "Q":
            os.system("clear")
            quit()
        elif terminal_input == "r" or terminal_input == "R":
            first_launch = True
            #TODO тут буде створення нового сіда
            pass
        elif terminal_input == "d" or terminal_input == "D":
            if os.path.exists("output_maze.txt"):
                os.remove("output_maze.txt")
                render_maze(matrix, width, height, i)
        else:
            os.system("clear")
            render_maze(matrix, width, height, i)




def main():
    width  = 30
    height = 30

    from oleh import MazeGenerator, text_png

    start_x, start_y = 0,0
    end_x, end_y = 10,18

    maze = MazeGenerator(width=width,
                         height=height,
                         entry_x=start_x,
                         entry_y=start_y,
                         exit_x=end_x,
                         exit_y=end_y,
                         text=text_png,
                         perfect=True)

    maze.generate_maze()
    maze_seed = str(maze)


    parser = argparse.ArgumentParser(description="A-Maze-Ing")
    parser.add_argument("--pretty", action="store_true", help="pretty maze")
    args = parser.parse_args()


    write_seed_to_file(maze_seed, width, height)
    write_coordinates_to_file(start_x, start_y, end_x, end_y)
    maze_run(maze_seed, width, height, start_x, start_y, end_x, end_y, args)




main()