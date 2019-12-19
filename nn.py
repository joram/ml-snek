#!/usr/bin/env python3
from PIL import Image
import os
import numpy
from keras.models import Sequential
from keras.layers import Dense


def gen_training_data():
    inputs = []
    outputs = []
    for filename in os.listdir("./images/"):
        filepath = os.path.join("./images/", filename)
        im = Image.open(filepath)
        pixels = im.load()
        w, h = im.size
        values = []
        for x in range(0, w):
            for y in range(0, h):
                val = pixels[x, y]
                values.append(val[0])
                values.append(val[1])
                values.append(val[2])
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


model = Sequential()
model.add(Dense(units=64, activation='relu', input_dim=363))
model.add(Dense(units=10, activation='softmax'))
model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='sgd',
    metrics=['accuracy'],
)
x_train, y_train = gen_training_data()
model.fit(x_train, y_train, epochs=1000, batch_size=500)

loss_and_metrics = model.evaluate(x_train, y_train, batch_size=128)
print(loss_and_metrics)

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
