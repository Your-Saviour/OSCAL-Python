# json_explorer.py
import json
import argparse
from typing import Any, Union
#import scripts.old.OSCAL_ISM_parser as OSCAL_ISM_parser

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

    
    #OSCAL_ISM_parser.main(data["catalog"], "catalog")
    print(data["catalog"].keys())
    for item in data["catalog"]["groups"]:
        print(item["title"])
        if item["title"] == "Cybersecurity terminology":
            break
        print(item["parts"] if "parts" in item.keys() else "")
        #print(item.keys())
        for item2 in item["groups"]:
            print("\t", item2["title"])
            print(item2["parts"] if "parts" in item2.keys() else "")
            #print("\t", item2.keys())
            if "groups" in item2.keys():
                for item3 in item2["groups"]:
                    print("\t\t",item3["title"])
                    print("\t\t", item3["parts"] if "parts" in item3.keys() else "")
                    #print("\t\t",item3.keys())
                    if "controls" in item3.keys():
                        for control in item3["controls"]:
                            print("\t"*3, control["id"])
                            #print("\t"*3, control.keys())

    


    



if __name__ == "__main__":
    main()