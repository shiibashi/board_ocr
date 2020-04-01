import os

if __name__ == "__main__":
    os.system("rm -rf annotation_data/0")
    os.system("rm -rf annotation_data/1")
    os.system("rm -rf annotation_data/2")
    os.system("rm -rf annotation_data/3")
    os.system("rm -rf annotation_data/4")
    os.system("rm -rf annotation_data/5")
    os.system("rm -rf annotation_data/6")
    os.system("rm -rf annotation_data/7")
    os.system("rm -rf annotation_data/8")
    os.system("rm -rf annotation_data/9")
    os.system("rm -rf annotation_data/10")
    os.system("rm -rf annotation_data/11")
    os.system("rm -rf annotation_data/12")
    data_list = os.listdir("annotation_data")
    via_data_list = [p for p in data_list if "via_project" in p]
    for via_data in via_data_list:
        s = via_data.replace(".json", "").replace("via_project_", "")
        jpg_data = "{}.jpg".format(s)
        json_filepath = "annotation_data/{}".format(via_data)
        jpg_filepath = "annotation_data/{}".format(jpg_data)
        shell = "python via_to_png.py --json_filepath {} --jpg_filepath {}".format(json_filepath, jpg_filepath)
        os.system(shell)
