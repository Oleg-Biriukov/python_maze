import argparse
# import MazeGenerator
from MazeVisualizer import (MazeApp, Maze, PrettyRenderer,
                            PlainRenderer, FileManager)
from MazeGenerator import text_png, MazeGenerator


# def extract_arg(filename: str) -> dict[str, any]:
#     arg = {
#         'WIDTH': None,
#         'HEIGHT': None,
#         'ENTRY': None,
#         'EXIT': None,
#         'OUTPUT_FILE': None,
#         'PERFECT': True}
#     try:
#         with open(filename, 'r') as conf:
#             for line in conf:
#                 if line[0] != '#':
#                     arg_val = line.split('=')
#                     if arg_val[0] in arg.keys() and len(arg_val) != 2:
#                         arg[arg_val[0]] = arg_val[1]
#                     else:
#                         raise ValueError('Wrong key was providen.')
#     except Exception as e:
#         print(f'{type(e).__name__}: {e}')
#         if type(e) is not FileNotFoundError:
#             print(f'''<format of {filename} file>
# KEY=VALUE
# KEY1=VALUE
# # comments provided, but it has to be in saparete line''')
#             exit(1)
#     return arg


def main() -> None:
    width = 30
    height = 30
    start_x = 0
    start_y = 0
    end_x = 10
    end_y = 10

    mazegen = MazeGenerator.MazeGenerator(width=width, height=height,
                                          perfect=False,
                                          text=text_png)

    mazegen.generate_maze()
    maze_seed = str(mazegen)
    print(maze_seed)

    parser = argparse.ArgumentParser(description="A-Maze-Ing")

    parser.add_argument("--pretty", action="store_true", help="pretty maze")

    args = parser.parse_args()

    maze = Maze(maze_seed, width, height, start_x, start_y, end_x, end_y)

    renderer = PrettyRenderer() if args.pretty else PlainRenderer()

    FileManager.save_initial_data(maze_seed, maze)

    app = MazeApp(maze, renderer)

    app.run()


if __name__ == "__main__":
    main()
