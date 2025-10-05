#Group #1 Guideline
#Group #2 Section
#Group #3 Topic
#Group #4 Control

def main(data : dict, json_path : str = ""):
    group_level = 1
    control_level = 1
    if "groups" in data.keys():
        for group in data["groups"]:
            json_path_new = json_path + f".group[{group_level}]"
            print(group["title"], json_path_new)
            main(group, json_path_new)
            group_level += 1
    elif "controls" in data.keys():
        for control in data["controls"]:
            json_path_new = json_path + f".controls[{control_level}]"
            [ print( x["prose"], json_path_new) for x in control["parts"]]
            control_level += 1

if __name__ == "__main___":
    pass