import imagehash
import json
import os
import pandas
import glob
import numpy
from PIL import Image
import time

from keras import models
from keras.models import Model
from keras import Input
from keras.layers import Activation, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.callbacks import TensorBoard, ModelCheckpoint
from sklearn.metrics import confusion_matrix

def read_json(json_filepath):
    with open(json_filepath, "r", encoding="utf-8") as f:
        d = json.load(f)
    return d

def load_dataset(label_dict):
    filepath_list = []
    phash_list = []
    label_list = []
    label_name_list = []
    for label_id, label_name in label_dict.items():
        data_path = "train_data/{}".format(label_id)
        filename_list = os.listdir(data_path)
        for filename in filename_list:
            filepath = "{}/{}".format(data_path, filename)
            img = Image.open(filepath).convert("L")
            phash = imagehash.phash(img)
            filepath_list.append(filepath)
            phash_list.append(phash)
            label_list.append(label_id)
            label_name_list.append(label_name)
    df = pandas.DataFrame(
        {"filepath": filepath_list, "phash": phash_list,
         "label_id": label_list, "label_name": label_name_list}
    )
    print("all_count={}".format(len(df)))
    df = df.drop_duplicates(subset=["phash"], keep="first").reset_index(drop=True)
    print("drop_duplicate_count={}".format(len(df)))
    print(df.groupby("label_id").count())
    return df

def train_test_split(df, label_dict):
    train_data_list = []
    test_data_list = []
    for label_id, label_name in label_dict.items():
        label_df = df[df["label_id"] == label_id].reset_index(drop=True)
        n = int(len(label_df) * 0.8)
        train_df = label_df.sample(n)
        test_index = [index for index in label_df.index if index not in train_df.index]
        test_df = label_df.loc[test_index]
        train_data_list.append(train_df)
        test_data_list.append(test_df)
    train_df = pandas.concat(train_data_list, axis=0).reset_index(drop=True)
    test_df = pandas.concat(test_data_list, axis=0).reset_index(drop=True)
    return train_df, test_df

def convert_nn_input(df, label_dict):
    x, y = [], []
    for i, row in df.sample(len(df)).iterrows():
        filepath = row["filepath"]
        label_id = row["label_id"]
        feature = load_ml_data(filepath)
        label_arr = convert_label_data(label_id, label_dict)
        x.append(feature)
        y.append(label_arr)
    x = numpy.array(x)
    y = numpy.array(y)
    return x, y

def load_ml_data(filepath):
    img = Image.open(filepath).convert("L").resize((20, 20))
    arr = (numpy.array(img) / 255.0).reshape(20, 20, 1)
    return arr

def convert_label_data(label_id, label_dict):
    return [1 if k == label_id else 0 for k, v in label_dict.items()]

def make_model_2(feature_shape, label_num):
    model = models.Sequential()
    model.add(Conv2D(2, (3, 3), padding='same', name='conv1', input_shape=(feature_shape[0], feature_shape[1], feature_shape[2])))
    model.add(Activation("relu", name='act1'))
    model.add(MaxPooling2D((2, 2), name='pool1'))
    model.add(Flatten(name='flatten'))
    model.add(Dense(label_num, name='dense1'))
    model.add(Activation('softmax', name='output'))
    return model
    
def make_model_3(feature_shape, label_num):
    model = models.Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu',
            input_shape=(feature_shape[0], feature_shape[1], feature_shape[2])))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(label_num, activation='softmax'))
    return model

def make_model(feature_shape, label_num):
    activation = 'relu'

    model = models.Sequential()

    model.add(Conv2D(32, (3, 3), padding='same', name='conv1',
            input_shape=(feature_shape[0], feature_shape[1], feature_shape[2])))
    model.add(Activation(activation, name='act1'))
    model.add(MaxPooling2D((2, 2), name='pool1'))

    model.add(Conv2D(64, (3, 3), padding='same', name='conv2'))
    model.add(Activation(activation, name='act2'))
    model.add(MaxPooling2D((2, 2), name='pool2'))

    model.add(Conv2D(64, (3, 3), padding='same', name='conv3'))
    model.add(Activation(activation, name='act3'))

    model.add(Flatten(name='flatten'))
    model.add(Dense(64, name='dense4'))
    model.add(Activation(activation, name='act4'))
    model.add(Dense(label_num, name='dense5'))
    model.add(Activation('softmax', name='last_act'))
    return model

def calc_cls_weight(df, label_dict):
    w = {}
    length = len(df)
    for label_id, label_name in label_dict.items():
        label_df = df[df["label_id"] == label_id].reset_index(drop=True)
        cnt = len(label_df)
        w[label_id] = 1.0 / cnt
    return w

def calc_score(pred, true):
    label_pred = pred.argmax(axis=1)
    label_true = true.argmax(axis=1)
    v = (label_pred == label_true).sum()
    return v / len(true)

if __name__ == "__main__":
    #json_filepath = "train_data/label.json"
    json_filepath = "train_data/label_only_number.json"
    label_dict = read_json(json_filepath)
    df = load_dataset(label_dict)
    print(len(df))
    print("_____")
    time.sleep(5)
    train_df, test_df = train_test_split(df, label_dict)
    weight_dict = calc_cls_weight(train_df, label_dict)
    train_x, train_y = convert_nn_input(train_df, label_dict)
    test_x, test_y = convert_nn_input(test_df, label_dict)
    feature_shape = (train_x.shape[1], train_x.shape[2], train_x.shape[3])
    label_num = len(label_dict)
    model = make_model(feature_shape, label_num)
    model.load_weights("model.hdf5")
    pred = model.predict(test_x)
    score = calc_score(pred, test_y)
    print(score)

    label_pred = pred.argmax(axis=1)
    label_true = test_y.argmax(axis=1)
    cm = confusion_matrix(label_true, label_pred)
    print(cm)
