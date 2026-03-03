import argparse
import os

width = 30
height = 30

parser = argparse.ArgumentParser(description="A-Maze-Ing")
parser.add_argument("--pretty", action="store_true", help="pretty maze")
parser.add_argument("filename", help="config file")
args = parser.parse_args()

if args.pretty:
    os.system(f"gnome-terminal --geometry={width*4+1}x{height*2+8} -- bash -c \
'python3 main.py --pretty config.txt'")
else:
    os.system(f"gnome-terminal --geometry={width*4+1}x{height*2+8} -- bash -c \
'python3 main.py config.txt'")
