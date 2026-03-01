import os
import argparse

width = 30
height = 30

parser = argparse.ArgumentParser(description="A-Maze-Ing")
parser.add_argument("--pretty", action="store_true", help="pretty maze")
args = parser.parse_args()

if args.pretty:
    os.system(f"gnome-terminal --geometry={width*4+1}x{height*2+7} -- bash -c 'python3 test.py --pretty'")
else:
    os.system(f"gnome-terminal --geometry={width*4+1}x{height*2+7} -- bash -c 'python3 test.py'")

