import bottle
import os
import heatMap
import pathing
import random
import Queue

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

def getOurSnake(data):
    SNAKE_ID = "6f8ded38-bd5c-41cf-b894-5b2152c1d8bd"
    ourSnake = None
    snakes = data['snakes']
    for snake in snakes:
        if snake["id"] == SNAKE_ID:
            ourSnake = snake
            break

    return ourSnake

def getSnakePosition(data):
    SNAKE_ID = "6f8ded38-bd5c-41cf-b894-5b2152c1d8bd"
    ourSnake = None
    snakes = data['snakes']
    for snake in snakes:
        if snake["id"] == SNAKE_ID:
            ourSnake = snake
            break
    return ourSnake['coords'][0]


@bottle.get('/')
def index():
    head_url = '%s://%s/static/dad.jpg' % (
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
        'taunt': ""
    }


def getGoal(data, position, width, height):
    Q = heatMap.getGoalQueue()
    dfs_grid = pathing.make_dfs_grid(data, width, height)
    visited = [[False for x in range(width)] for x in range(height)]
    goal = Q.get()
    while not pathing.is_path(dfs_grid, visited, position, [goal[1], goal[2]], width, height):
        if Q.empty():
            print("PANIC")
            return goal
        goal = Q.get()
    return goal

@bottle.post('/move')
def move():

    taunts = [
        'That\'s not a good to get a head',
        'Donut be angry',
        'I had a pizza joint once. It didn\'t pan out',
        'Don\'t call me later.  Call me dad.',
        'What time is it? I don\'t know, it keeps changing.',

    ]

    data = bottle.request.json

    height = data["height"]
    width = data["width"]

    ourHeatMap = heatMap.heatMap(width, height)
    board = ourHeatMap.getHeatMap(data, getOurSnake(data))
    position = getSnakePosition(data)
    goal = getGoal(data, position, width, height)
    board[position[0]][position[1]] = 1000000

    direction = pathing.find_path_direction(board, width, height, position, goal)
    print board
    print position
    print goal
    print direction

    return {
        'move': direction,
        'taunt': random.choice(taunts)
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
