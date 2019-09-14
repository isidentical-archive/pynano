import argparse
from pathlib import Path

from pynano.pyn import PyNano


def main(file, backend=None):
    if not file.exists():
        raise FileNotFoundError(f"{file} not found!")

    pynano = PyNano()
    result = pynano.compile(file, backend=backend)
    print(result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PyNano")
    parser.add_argument("file", type=Path, help="pynano file to run")
    parser.add_argument("backend", default=None, nargs="?", help="compilation target")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
