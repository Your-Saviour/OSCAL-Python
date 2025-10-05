# json_explorer.py
import json
import argparse
from typing import Any, Union

def explore_json(data: Union[dict, list], indent: int = 0, max_depth: int = 5):
    """
    Recursively explore and print JSON keys/values up to max_depth.
    """
    prefix = "  " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)) and indent < max_depth:
                print(f"{prefix}{key}:")
                explore_json(value, indent + 1, max_depth)
            else:
                preview = str(value)
                if len(preview) > 60:
                    preview = preview[:57] + "..."
                print(f"{prefix}{key}: {preview}")
    elif isinstance(data, list):
        for idx, item in enumerate(data[:10]):  # show only first 10 elements
            if isinstance(item, (dict, list)) and indent < max_depth:
                print(f"{prefix}[{idx}]:")
                explore_json(item, indent + 1, max_depth)
            else:
                preview = str(item)
                if len(preview) > 60:
                    preview = preview[:57] + "..."
                print(f"{prefix}[{idx}]: {preview}")
        if len(data) > 10:
            print(f"{prefix}... ({len(data)} items total)")


def main():
    parser = argparse.ArgumentParser(description="Explore JSON structures interactively.")
    parser.add_argument("file", help="Path to JSON file")
    parser.add_argument("--max-depth", type=int, default=5, help="Max depth to explore (default: 5)")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        data = json.load(f)

    explore_json(data, max_depth=args.max_depth)


if __name__ == "__main__":
    main()
