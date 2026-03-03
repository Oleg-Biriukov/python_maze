import argparse
from .umodels import Maze, FileManager
from .views import PlainRenderer, PrettyRenderer, MazeApp
from MazeGenerator.MazeGenerator import MazeGenerator
from MazeGenerator import text_png


def main() -> None:
    width = 30
    height = 30
    start_x = 0
    start_y = 0
    end_x = 10
    end_y = 10

    mazegen = MazeGenerator(width=width, height=height, perfect=False,
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
