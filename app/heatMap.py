class heatMap:

    def __init__(self, width, height):
        self.goal = [1,1]
        self.aroundSnake = 5
        self.width = width
        self.height = height
        self.board = [[1 for x in range(self.width)] for x in range(self.height)]

    def fillSnakes(self, data):
        for snake in data:
            coordinates = snake['coords']
            for cord in coordinates:
                x = cord[0]
                y = cord[1]
                self.board[x][y] = None
                self.fillRadius(x,y,1,self.aroundSnake)



    def fillRadius(self, x, y, radius, radiusAmount):
        radius -= 1
        coordinates = [[x-1, y], [x+1,y], [x, y+1], [x,y-1], [x+1, y+1], [x+1, y-1], [x-1, y+1], [x-1, y-1]]
        for point in coordinates:
            xx = point[0]
            yy = point[1]
            if (self.board[xx][yy]) != None:
                        self.board[xx][yy] += radiusAmount
        if radius > 0:
            for point in coordinates:
                self.fillRadius(point[0], point[1], radius, radiusAmount)



    def fillBorder(self):
        for i in range(0, self.width):
            self.board[i][0] = None
            self.board[i][self.height-1] = None
        for i in range(0, self.height):
            self.board[0][i] = None
            self.board[self.width-1][i] = None


    def fillHeatMap(self, data):
        self.fillSnakes(data['snakes'])
        #self.fillBorder()

    def getGoal(self):
        return self.goal

    def getHeatMap(self, data):
        self.fillHeatMap(data)
        return self.board
