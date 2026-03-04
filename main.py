import argparse
from MazeVisualizer import (MazeApp, Maze, PrettyRenderer,
                            PlainRenderer, FileManager)
from MazeGenerator import text_png, MazeGenerator
from pydantic import ValidationError
from typing import cast


def main() -> None:
    parser = argparse.ArgumentParser(description="A-Maze-Ing")

    parser.add_argument("--pretty", action="store_true", help="pretty maze")

    parser.add_argument("filename", help="name of config")

    args = parser.parse_args()

    if conf := FileManager.extract_arg(args.filename):
        exit: tuple[int, ...] = cast(tuple[int, ...], conf['EXIT'])
        entry: tuple[int, ...] = cast(tuple[int, ...], conf['ENTRY'])
        width: int = cast(int, conf['WIDTH'])
        height: int = cast(int, conf['HEIGHT'])
        start_x: int = cast(int, entry[0])
        start_y: int = cast(int, entry[1])
        end_x: int = cast(int, exit[0])
        end_y: int = cast(int, exit[1])
        name: str = cast(str, conf['OUTPUT_FILE'])
        perfect: bool = cast(bool, conf['PERFECT'])
        if name:
            FileManager.modify_filename(name)

        def create_maze() -> Maze | None:
            """Maze generation function"""
            try:
                if (start_x >= width or start_y >= height
                    or end_x >= width or end_y >= height
                        or conf['ENTRY'] == conf['EXIT']):
                    raise ValueError('The coordinates of exit or entry was \
provided wrong')

                mazegen = MazeGenerator.MazeGenerator(
                    width=width,
                    height=height,
                    perfect=perfect,
                    text=text_png
                )

                mazegen.generate_maze()
                maze_seed = str(mazegen)
                new_maze = Maze(
                    maze_seed,
                    width, height,
                    start_x, start_y,
                    end_x, end_y
                )

                FileManager.save_initial_data(maze_seed, new_maze)

                return new_maze
            except Exception as e:
                if isinstance(e, ValidationError):
                    for err in e.errors():
                        print(f'''Error detected during compilation maze:
{type(e).__name__} === {err['msg']}''')
                else:
                    print(f'''Error detected during compilation maze:
{type(e).__name__} === {e}''')
                return None

        if maze := create_maze():

            renderer = PrettyRenderer() if args.pretty else PlainRenderer()

            app = MazeApp(maze, renderer, regenerate_func=create_maze)

            app.run()


if __name__ == "__main__":
    main()
