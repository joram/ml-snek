#!/usr/bin/env python3
import numpy
import json
import boto3
from PIL import Image


def all_games():
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket("jsnek")
    for obj in my_bucket.objects.all():
        content = obj.get()['Body'].read()
        try:
            yield json.loads(content)
        except:
            pass


def frame_to_image(frame, next_frame, winner_id):
    w = frame["board"]["height"]
    h = frame["board"]["width"]
    array = numpy.zeros([w, h, 3], dtype=numpy.uint8)

    # body
    for snake in frame["board"]["snakes"]:
        body = snake["body"]
        for i in range(0, len(body)):
            coord = body[i]
            array[coord["x"], coord["y"]] = [255 - len(body) + i, 0, 0]

    # food
    foods = frame["board"]["food"]
    for coord in foods:
        array[coord["x"], coord["y"]] = [0, 255, 0]

    # head
    head = None
    for snake in frame["board"]["snakes"]:
        if snake["id"] == winner_id:
            head = snake["body"][0]
            break

    next_head = None
    for snake in next_frame["board"]["snakes"]:
        if snake["id"] == winner_id:
            next_head = snake["body"][0]
            break

    array[head["x"], head["y"]] = [0, 0, 255]
    delta_x = next_head["x"] - head["x"]
    delta_y = next_head["y"] - head["y"]

    try:
        direction = {
            (0, 1): "UP",
            (0, -1): "DOWN",
            (1, 0): "RIGHT",
            (-1, 0): "LEFT"
        }[(delta_x, delta_y)]
        filename = f'../images/{frame["game"]["id"]}_{frame["turn"]}::{direction}.png'
        img = Image.fromarray(array)
        img.save(filename)
        return filename
    except Exception as e:
        return "???"


for game in all_games():
    snakes = game[-1]["board"]["snakes"]
    if len(snakes) == 0:
        continue
    winner_id = snakes[0]["id"]
    for i in range(0, len(game)-1):
        frame = game[i]
        next_frame = game[i+1]
        filename = frame_to_image(frame, next_frame, winner_id)
    print(game[0]["game"]["id"])
