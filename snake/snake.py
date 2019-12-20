#!/usr/bin/env python3
from nn import load_model
import json
from Pillow import Image
import os
import bottle
from api import ping_response, start_response, move_response, end_response
import numpy

model = load_model()


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.
    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


def _make_pixels(data):
    im = Image.new('RGB', (data["board"]["width"], data["board"]["height"]), color=(0, 0, 0))
    pixels = im.load()

    # age of body
    for snake in data["board"]["snakes"]:
        i = 0
        for c in snake["body"]:
            curr = pixels[c["x"], c["y"]]
            curr[0] = len(snake["body"]) - i
            pixels[c["x"], c["y"]] = curr
            i += 1

    # food
    for food in data["board"]["food"]:
        pixels[food["x"], food["y"]] = (0, 255, 0)

    # my head
    head = data["you"]["body"][0]
    pixels[head["x"], head["y"]] = (0, 0, 255)
    return pixels


@bottle.post('/move')
def move():
    data = bottle.request.json
    print(json.dumps(data))
    pixels = _make_pixels(data)

    directions = ['up', 'down', 'left', 'right']
    p = model.predict_classes(numpy.array([pixels]))
    prediction = p[0]
    direction = directions.index(prediction)
    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()


if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )

