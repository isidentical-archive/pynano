import argparse
from pathlib import Path

from pynano.pyn import PyNano


def main(file):
    if not file.exists():
        raise FileNotFoundError(f"{args.file} not found!")

    pynano = PyNano()
    pynano.compile(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PyNano")
    parser.add_argument("file", type=Path, help="pynano file to run")
    args = parser.parse_args()
    main(**vars(args))
