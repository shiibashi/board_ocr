import json
from PIL import Image
import os
import argparse
import copy

def _argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_json_filepath', help='target_via_project_filepath',
                        required=True)
    parser.add_argument('--output_dirpath', help='output_via_project_dirpath',
                        required=True)
    args = parser.parse_args()
    return args

def read_json(json_filepath):
    with open(json_filepath, "r", encoding="utf-8") as f:
        d = json.load(f)
    return d

def write_json(json_data, json_filepath):
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)

def read_jpg(jpg_filepath):
    img = Image.open(jpg_filepath)
    return img

def number_0(region, source_json_filepath):
    if "via_project_test2.json" in source_json_filepath:
        shape = region["shape_attributes"]
        x = shape["x"]
        y = shape["y"]
        width = shape["width"]
        height = shape["height"]
        if 539 <= x <= 555 or 723 <= x <= 737:
            return {"number": "0"}
        else:
            return {}
    else:
        return {}

def area4():
    over_area = [
{'name': 'rect', 'x': 516, 'y': 203, 'width': 6, 'height': 15},
{'name': 'rect', 'x': 522, 'y': 203, 'width': 6, 'height': 15},
{'name': 'rect', 'x': 528, 'y': 203, 'width': 5, 'height': 15},
{'name': 'rect', 'x': 534, 'y': 203, 'width': 6, 'height': 15},
{'name': 'rect', 'x': 541, 'y': 203, 'width': 6, 'height': 15},
{'name': 'rect', 'x': 546, 'y': 203, 'width': 6, 'height': 14}
    ]
    under_area = [
{'name': 'rect', 'x': 699, 'y': 736, 'width': 7, 'height': 14},
{'name': 'rect', 'x': 705, 'y': 736, 'width': 7, 'height': 13},
{'name': 'rect', 'x': 712, 'y': 736, 'width': 6, 'height': 13},
{'name': 'rect', 'x': 718, 'y': 736, 'width': 6, 'height': 13},
{'name': 'rect', 'x': 724, 'y': 736, 'width': 6, 'height': 13},
{'name': 'rect', 'x': 730, 'y': 736, 'width': 6, 'height': 13}
    ]
    upper_price_area = [
{'name': 'rect', 'x': 606, 'y': 462, 'width': 7, 'height': 13},
{'name': 'rect', 'x': 612, 'y': 462, 'width': 7, 'height': 13},
{'name': 'rect', 'x': 618, 'y': 461, 'width': 7, 'height': 14},
{'name': 'rect', 'x': 625, 'y': 462, 'width': 7, 'height': 13}
    ]
    downer_price_area = [
{'name': 'rect', 'x': 606, 'y': 478, 'width': 6, 'height': 13},
{'name': 'rect', 'x': 612, 'y': 477, 'width': 7, 'height': 14},
{'name': 'rect', 'x': 618, 'y': 477, 'width': 7, 'height': 14},
{'name': 'rect', 'x': 625, 'y': 478, 'width': 7, 'height': 13}
    ]
    return over_area, under_area, upper_price_area, downer_price_area


if __name__ == "__main__":
    #target_json_filepath = "via_project.json"
    #output_json_filepath = "via_project_before_annotation.json"

    args = _argparse()
    target_json_filepath = args.target_json_filepath
    output_dirpath = args.output_dirpath
    os.makedirs(output_dirpath, exist_ok=True)
    target_json_data = read_json(target_json_filepath)
    
    over_area, under_area, upper_price_area, downer_price_area = area4()
    area_list = over_area + under_area + upper_price_area + downer_price_area
    
    region_data = [{"shape_attributes": area, "region_attributes": {"number":"1"}} for area in area_list]

    for k, d in target_json_data["_via_img_metadata"].items():
        target_json_data["_via_img_metadata"][k]["regions"] = region_data
        filename_without_suffix = k.split(".")[0]            
    output_json_filepath = "{}/via_project_{}.json".format(output_dirpath, filename_without_suffix)
    write_json(target_json_data, output_json_filepath)
