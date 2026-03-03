import argparse
from MazeVisualizer import (MazeApp, Maze, PrettyRenderer,
                            PlainRenderer, FileManager)
from MazeGenerator import text_png, MazeGenerator


def main() -> None:
    parser = argparse.ArgumentParser(description="A-Maze-Ing")

    parser.add_argument("--pretty", action="store_true", help="pretty maze")

    parser.add_argument("filename", help="name of config")

    args = parser.parse_args()

    if conf := FileManager.extract_arg(args.filename):
        width = conf['WIDTH']
        height = conf['HEIGHT']
        start_x, start_y = conf['ENTRY']
        end_x, end_y = conf['EXIT']
        mazegen = MazeGenerator.MazeGenerator(width=width, height=height,
                                              perfect=conf['PERFECT'],
                                              text=text_png)

        mazegen.generate_maze()
        maze_seed = str(mazegen)
        print(maze_seed)

        maze = Maze(maze_seed, width, height, start_x, start_y, end_x, end_y)

        renderer = PrettyRenderer() if args.pretty else PlainRenderer()

        FileManager.modify_filename(conf['OUTPUT_FILE'])
        FileManager.save_initial_data(maze_seed, maze)

        app = MazeApp(maze, renderer)

        app.run()


if __name__ == "__main__":
    main()
