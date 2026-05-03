# main.py

import argparse

from presets import PRESETS
from renderer import draw_cover


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--preset", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--output", default="cover.webp")

    args = parser.parse_args()

    params = PRESETS.get(args.preset)

    if not params:
        raise ValueError("Invalid preset")

    draw_cover(params, args.name, args.output)


if __name__ == "__main__":
    main()
