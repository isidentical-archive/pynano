import argparse
from pathlib import Path

def main(file):
    if not file.exists():
        raise FileNotFoundError(f"{args.file} not found!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PyNano")
    parser.add_argument(
        "file", type=Path, help="pynano file to run"
    )
    args = parser.parse_args()
    main(**vars(args))
    
