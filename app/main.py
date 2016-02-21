import bottle
import os
import heatMap
import pathing

SNAKE_ID = "6f8ded38-bd5c-41cf-b894-5b2152c1d8bd"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


def getSnakePosition(data):
    snakes = data['snakes']
    ourSnake = snakes[SNAKE_ID]
    return ourSnake['coords'][0]


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00ff00',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    height = data["height"]
    width = data["width"]

    ourHeatMap = heatMap.heatMap(width, height)
    board = ourHeatMap.getHeatMap(data)
    goal = ourHeatMap.getGoal()
    position = getSnakePosition(data)

    direction = pathing.find_path_direction(board, board.width, board.height, position, goal)
    print board
    print position
    print goal
    print direction

    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
