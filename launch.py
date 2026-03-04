import argparse
import os
from MazeVisualizer import FileManager
from typing import cast

parser = argparse.ArgumentParser(description="A-Maze-Ing")
parser.add_argument("--pretty", action="store_true", help="pretty maze")
parser.add_argument("filename", help="config file")
args = parser.parse_args()
if conf := FileManager.extract_arg(args.filename):
    width: int = cast(int, conf['WIDTH'])
    height: int = cast(int, conf['HEIGHT'])
    if args.pretty:
        os.system(f"gnome-terminal --geometry={width*4+1}x{height*2+9} \
-- bash -c 'python3 main.py --pretty config.txt'")
    else:
        os.system(f"gnome-terminal --geometry={width*4+1}x{height*2+9} \
-- bash -c 'python3 main.py config.txt'")
