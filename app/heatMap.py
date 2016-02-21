class heatMap:

    def __init__(self, width, height):
        self.goal = [1,1]
        self.aroundSnake = 5
        self.width = width
        self.height = height
        self.board = [[2 for x in range(self.width)] for x in range(self.height)]

    def fillSnakes(self, data, ourSnake):
        for snake in data:
            coordinates = snake['coords']
            for cord in coordinates:
                x = cord[0]
                y = cord[1]
                self.board[x][y] = None
                self.fillRadius(x,y,1,self.aroundSnake)
            print ourSnake
            if ourSnake["food"] > snake["food"]:
                x = coordinates[0][0]
                y = coordinates[0][1]
                self.board[x][y] = 0


    def fillRadius(self, x, y, radius, radiusAmount):
        radius -= 1
        coordinates = [[x-1, y], [x+1,y], [x, y+1], [x,y-1], [x+1, y+1], [x+1, y-1], [x-1, y+1], [x-1, y-1]]
        for point in coordinates:
            xx = point[0]
            yy = point[1]
            if xx < 0 or xx >= self.width:
                continue
            if yy < 0 or yy >= self.height:
                continue

            if (self.board[xx][yy]) != None:
                        self.board[xx][yy] = radiusAmount
        if radius > 0:
            for point in coordinates:
                self.fillRadius(point[0], point[1], radius, radiusAmount)


    def fillHeatMap(self, data, ourSnake):
        self.fillSnakes(data['snakes'], ourSnake)
        self.fillFood(data['food'])

    def fillFood(self, data):
        for food in data:
            self.board[food[0]][food[1]] = min(self.board[food[0]][food[1]], 1)

    def findSmallestCoordinate(self):
        min = 10000
        x = None
        y = None
        for i in range(0,self.width):
            for j in range(0,self.height):
                if self.board[i][j] < min and self.board[i][j] is not None:
                    min = self.board[i][j]
                    x = i
                    y = j
        return [x,y]

    def getGoal(self):
        return self.findSmallestCoordinate()

    def getHeatMap(self, data, ourSnake):
        self.fillHeatMap(data, ourSnake)
        return self.board
