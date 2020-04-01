import json
from PIL import Image
import os
import argparse

def _argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_filepath', help='via_project_filepath', required=True)
    parser.add_argument('--jpg_filepath', help='image_filepath', required=True)
    args = parser.parse_args()
    return args

def read_json(json_filepath):
    with open(json_filepath, "r", encoding="utf-8") as f:
        d = json.load(f)
    return d

def read_jpg(jpg_filepath):
    img = Image.open(jpg_filepath)
    return img

def extract_label_dict(json_data):
    return json_data["_via_attributes"]["region"]["number"]["options"]
    
def crop_annotation_region(image, p1, p2):
    cropped = image.crop((p1[0], p1[1], p2[0], p2[1]))
    return cropped

def save_annotation_image(regions, filename):
    for i, region in enumerate(regions):
        shape_attributes = region["shape_attributes"]
        shape = shape_attributes["name"]
        assert shape == "rect"
        x = shape_attributes["x"]
        y = shape_attributes["y"]
        width = shape_attributes["width"]
        height = shape_attributes["height"]
        if width < 3 or height < 3:
            continue
        region_attributes = region["region_attributes"]
        label_id = region_attributes["number"]
        p1 = (x, y)
        p2 = (x+width, y+height)
        cropped_image = crop_annotation_region(image, p1, p2)
        filepath = "{}_{}.jpg".format(filename, i)
        cropped_image.save("train_data/{}/{}".format(label_id, filepath))

if __name__ == "__main__":
    args = _argparse()
    json_data = read_json(args.json_filepath)
    image = read_jpg(args.jpg_filepath)
    label_dict = extract_label_dict(json_data)
    for label_id, label_name in label_dict.items():
        os.makedirs("train_data/{}".format(label_id), exist_ok=True)

    for f, metadata in json_data["_via_img_metadata"].items():
        filename = metadata["filename"]
        filename_without_suffix = filename.split(".")[0]
        regions = metadata["regions"]
        save_annotation_image(regions, filename_without_suffix)