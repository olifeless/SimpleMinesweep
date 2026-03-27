import random as r


class EventManager():

    start = False
    dead = False



    def __init__(self, x, y):
        self.__squares = {}
        self.__timer = []
        self.__flagCounter = []
        self.__face = None
        self.__pressedKeys = set()
        self.__clicked = set() #Not in use, was going to use to check which mouse buttons are currently held down
        self.__scan = False
        self.__totalMines = 0
        self.__mX = x
        self.__mY = y

    def registerSq(self, sprite, x, y):
        if x not in self.__squares:
            self.__squares[x] = []
        self.__squares[x].append(sprite)


    def addTimer(self, sprite):
        self.__timer.append(sprite)

    def addFlagCounter(self, sprite):
        self.__flagCounter.append(sprite)

    def addface(self, sprite):
        self.__face = sprite


    def initialiseMines(self):
        while self.__totalMines < 100:
            xCoord = r.randint(0, self.__mX -1)
            yCoord = r.randint(0, self.__mY -1)
            if self.__squares[xCoord][yCoord].setMineState():
                self.__totalMines += 1
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= xCoord+i < self.__mX and 0 <= yCoord + j < self.__mY:
                            self.__squares[xCoord+i][yCoord+j].addAdjMines()

    def fixMines(self, e, x, y):
        EventManager.start = True
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x+i < self.__mX and 0 <= y + j < self.__mY:
                    if self.__squares[x + i][y + j].getMines():
                        self.__squares[x+i][y+j].removeMine()
                        self.__totalMines -= 1
                        for k in range(-1, 2):
                            for l in range(-1, 2):
                                if 0 <= x+i+k < self.__mX and 0 <= y+j+l < self.__mY:
                                    self.__squares[x+i+k][y+j+l].removeAdjMines()
                        self.initialiseMines()
        for i in self.__squares:
            for sq in self.__squares[i]:
                sq.bindInput()
        self.__squares[x][y].clicked(0)
        self.__timer[0].startThread() #Starts timer
        #Maybe dont nest 4 loops?


    def checkNeighbour(self, x, y):
        for i in range(-1,2):
            for j in range(-1,2):
                if 0 <= x+i < self.__mX and 0 <= y+j < self.__mY:
                    if not self.__squares[x+i][y+j].getState():
                        self.__squares[x+i][y+j].clicked(0)

        
    def resetSq(self, e):
        if EventManager.start:
            for i in self.__squares:
                for sq in self.__squares[i]:
                    sq.reset()
                    sq.until_I_Can_Think_Of_Other_Solutions_This_Is_The_Only_Way()
            self.__totalMines = 0
            self.initialiseMines()
            for i in self.__timer:
                i.restart()
            self.__flagCounter[0].reset()
            self.__face.reset()
            EventManager.start = False
            EventManager.dead = False

    def death(self):
        EventManager.dead = True
        self.__timer[0].stop()
        self.__face.over()
        for i in self.__squares:
            for sq in self.__squares[i]:
                sq.gameOver()


    def completed(self):
        if EventManager.dead:
            return
        self.__timer[0].stop()
        self.__face.completed()
        for i in self.__squares:
            for sq in self.__squares[i]:
                if not sq.getFlagged():
                    if not sq.getMines():
                        raise Exception("Shouldve ended but theres still clear space unrevealed")
                    else:
                        sq.flag()

    def scan(self, x, y, mines):
        a = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x+i < self.__mX and 0 <= y+j < self.__mY:
                    if self.__squares[x+i][y+j].getFlagged():
                        a += 1
        if a == mines:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= x+i <= self.__mX and 0 <= y+j <= self.__mY:
                        self.__squares[x+i][y+j].clicked(0)


    def onPressed(self, e, x, y): #Not in use
        self.__clicked.add(e.num)
        if e.num == 1 and not self.__scan:
            self.__squares[x][y].tempChange()
        elif e.num == 3 and not self.__scan:
            self.__squares[x][y].flag()
        if 1 in self.__clicked and 3 in self.__clicked:
            for i in range(-1,2):
                for j in range(-1,2):
                    if 0 <= x+i < self.__mX and 0 <= y + j < self.__mY:
                        self.__squares[x+i][y+j].tempChange()
                        self.__scan = True
            #self.scan(x, y, self.__squares[x][y].getAdjMines())

    def onReleased(self, e, x, y): #Not in use
        self.__clicked.discard(e.num)
        if e.num == 1 and not self.__scan:
            self.__squares[x][y].clicked()
            print("I tried")
        if e.num in [1,3] and (1 not in self.__clicked or 3 not in self.__clicked):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    self.__squares[x][y].tempChange()
    

    def broadcastChangeSkin(self, s=str):
        #Change skin, specified by "t" for Timer, and "f" for flag-count
        if s == "t":
            for t in self.__timer:
                t.changeSkin()
        elif s == "f":
            for f in self.__flagCounter:
                f.changeSkin()
    
    def broadcastFlag(self, flagged=bool): #For flag counter sprite
        if flagged:
            self.__flagCounter[0].flagged()
        else:
            self.__flagCounter[0].unflagged()
    
