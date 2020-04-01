import json
from PIL import Image
import os
import argparse
import copy

def _argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_json_filepath', help='target_via_project_filepath',
                        required=True)
    parser.add_argument('--source_json_filepath', help='source_via_project_filepath',
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

if __name__ == "__main__":
    #target_json_filepath = "via_project.json"
    #source_json_filepath = "annotation_tool/sample_data/via_project_sample.json"
    #output_json_filepath = "via_project_before_annotation.json"

    args = _argparse()
    target_json_filepath = args.target_json_filepath
    source_json_filepath = args.source_json_filepath
    output_dirpath = args.output_dirpath
    os.makedirs(output_dirpath, exist_ok=True)
    target_json_data = read_json(target_json_filepath)
    source_json_data = read_json(source_json_filepath)

    for filename, metadata in source_json_data["_via_img_metadata"].items():
        
        # source_json_dataからregionデータの取得
        region_data = copy.deepcopy(metadata["regions"])
        for region in region_data:
            region["region_attributes"] = number_0(region, source_json_filepath)

        # target_json_dataにregionデータを入力
        for k, d in target_json_data["_via_img_metadata"].items():
            target_json_data["_via_img_metadata"][k]["regions"] = region_data
            filename_without_suffix = k.split(".")[0]
        output_json_filepath = "{}/via_project_{}.json".format(output_dirpath, filename_without_suffix)
        write_json(target_json_data, output_json_filepath)
        break
