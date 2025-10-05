# json_explorer.py
import json
import argparse
from typing import Any, Union
import OSCAL_ISM_parser

def recursive_groups(data : dict, json_path : str, level : int = 0):
    level = level + 1
    group_level = 1
    control_level = 1
    try:
        for group in data["groups"]:
            print(level * "--", group["title"])
            json_path_new = json_path + f".group[{group_level}]"
            recursive_groups(group, json_path_new, level)
            group_level += 1
    except Exception as e:
        #print(type(data))
        #print(data.keys())
        if "controls" in data.keys():
            for group in data["controls"]:
                json_path_new = json_path + f".control[{control_level}]"
                print(level * "--", group["title"])
                [ print(level * "--" , x["prose"], json_path_new) for x in group["parts"]]
                control_level = control_level + 1
    print()


def main():
    parser = argparse.ArgumentParser(description="Explore JSON structures interactively.")
    parser.add_argument("file", help="Path to JSON file")

    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        data = json.load(f)

    
    OSCAL_ISM_parser.main(data["catalog"], "catalog")

    


    



if __name__ == "__main__":
    main()