#!/usr/bin/env python3
from PIL import Image
import os
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json


def image_to_input(pixels, w, h):
    values = []
    for x in range(0, w):
        for y in range(0, h):
            val = pixels[x, y]
            values.append(val[0])
            values.append(val[1])
            values.append(val[2])
    return values


def gen_training_data():
    inputs = []
    outputs = []
    for filename in os.listdir("../images/"):
        filepath = os.path.join("../images/", filename)
        im = Image.open(filepath)
        pixels = im.load()
        w, h = im.size
        values = image_to_input(pixels, w, h)
        directions = ["up", "down", "left", "right"]
        try:
            direction = filename.split("::")[1].replace(".jpg", "")
            d = directions.index(direction)
            outputs.append([d])
            inputs.append(values)
        except Exception as e:
            pass

    print(len(inputs), len(outputs))
    return numpy.array(inputs), numpy.array(outputs)


def make_model():
    model = Sequential()
    model.add(Dense(units=128, activation='relu', input_dim=363))
    model.add(Dense(units=32, activation='softmax'))
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer='sgd',
        metrics=['accuracy'],
    )
    return model


def load_model(filepath="model.h5"):
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")


def train_model(model, save_filepath="model.h5"):
    x_train, y_train = gen_training_data()
    model.fit(x_train, y_train, epochs=100, batch_size=50)

    loss_and_metrics = model.evaluate(x_train, y_train, batch_size=128)
    print(loss_and_metrics)

    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights(save_filepath)

    wins = 0
    losses = 0
    for i in range(0, len(x_train)):
        p = model.predict_classes(numpy.array([x_train[i]]))
        prediction = p[0]
        desired = y_train[i][0]
        if prediction == desired:
            wins += 1
        else:
            losses += 1
    print(f"wins {wins}\t losses {losses}\t total {wins+losses}")


if __name__ == "__main__":
    model = make_model()
    train_model(model)
