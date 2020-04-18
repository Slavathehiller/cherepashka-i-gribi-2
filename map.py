from random import*
from mole import*
from Options import *
from math import*
from mushroom import*
from obstacle import*
import winsound

class MapManager:
    sizeY = 5
    sizeX = 5
    Map = list()
    OutMap = None
    turtle = None
    obstacles = []
    moles = []
    mushrooms = []
    obstaclesNumber = 0
    molesNumber = 0
    mushroomNumber = 0

    def __init__(self, vidget, turtle, options):
        self.OutMap = vidget
        self.turtle = turtle
        self.molesNumber = options.MoleCount
        self.mushroomNumber = options.MushroomCount
        self.obstaclesNumber = options.ObstacleCount
        self.sizeY = options.sizeY
        self.sizeX = options.sizeX
        self.InitMap()

    def distanceToTurtle(self, x, y):
        return sqrt((self.turtle.x - x) ** 2 + (self.turtle.y - y) ** 2)

    def isTurtle(self, x, y):
        return self.turtle.x == x and self.turtle.y == y

    def isMole(self, x, y):
        for mole in self.moles:
            if mole.x == x and mole.y == y:
                return True
        return False

    def isOut(self, x, y):
        return x < 0 or y < 0 or x > self.sizeX - 1 or y > self.sizeY - 1

    def isObstacle(self, x, y):
        for obstacle in self.obstacles:
            if obstacle.x == x and obstacle.y == y:
                return True
        return False

    def isMushroom(self, x, y):
        for mushroom in self.mushrooms:
            if mushroom.x == x and mushroom.y == y:
                return True
        return False


    def isObstacleOrOut(self, x, y):
        return self.isObstacle(x, y) or self.isOut(x, y)

    def isFree(self, x, y):
        return not self.isMushroom(x, y) and not self.isTurtle(x, y) and not self.isObstacleOrOut(x, y) and not self.isMole(x, y)

    def isAvaliableforMole(self, x, y):
        return not self.isTurtle(x, y) and not self.isMole(x, y)

    def isAvaliableforMushroom(self, x, y):
        return self.isFree(x, y)


    def isMoleCanMove(self, mole, direction):
        tryX, tryY = mole.x, mole.y
        if direction == Up:
            tryY = tryY - 1
        if direction == Down:
            tryY = tryY + 1
        if direction == Left:
            tryX = tryX - 1
        if direction == Right:
            tryX = tryX + 1
        return self.isFree(tryX, tryY) or self.isTurtle(tryX, tryY)

    def isTurtleCanMove(self, direction):
        tryX, tryY = self.turtle.x, self.turtle.y
        if direction == Up:
            tryY = tryY - 1
        if direction == Down:
            tryY = tryY + 1
        if direction == Left:
            tryX = tryX - 1
        if direction == Right:
            tryX = tryX + 1
        return self.isFree(tryX, tryY) or self.isMushroom(tryX, tryY) or self.isMole(tryX, tryY)

    def placeObstacles(self):
        self.obstacles = []
        for i in range(self.obstaclesNumber):
             obstacle = Obstacle(randint(0, self.sizeX - 1), randint(0, self.sizeY - 1))
             while not self.isAvaliableforMole(obstacle.x, obstacle.y):
                 obstacle.x = randint(0, self.sizeX - 1)
                 obstacle.y = randint(0, self.sizeY - 1)
             self.obstacles.append(obstacle)


    def placeMoles(self):
        self.moles = []
        for i in range(self.molesNumber):
             mole = Mole()
             mole.x = randint(0, self.sizeX - 1)
             mole.y = randint(0, self.sizeY - 1)
             while not self.isAvaliableforMole(mole.x, mole.y):
                 mole.x = randint(0, self.sizeX - 1)
                 mole.y = randint(0, self.sizeY - 1)
             self.moles.append(mole)

    def placeMushrooms(self):
        self.mushrooms = []
        for i in range(self.mushroomNumber):
            mushroom = Mushroom(randint(0, self.sizeX - 1), randint(0, self.sizeY - 1))
            while not self.isAvaliableforMushroom(mushroom.x, mushroom.y):
                mushroom.x = randint(0, self.sizeX - 1)
                mushroom.y = randint(0, self.sizeY - 1)
            self.mushrooms.append(mushroom)

    def checkAndEat(self):
        if self.isMole(self.turtle.x, self.turtle.y):
            self.drawMap()
            return LOSE
        for i in range(len(self.mushrooms)):
            if self.isTurtle(self.mushrooms[i].x, self.mushrooms[i].y):
                del self.mushrooms[i]
                winsound.PlaySound("Niam.wav", winsound.SND_ASYNC + winsound.SND_PURGE)
                self.drawMap()
                if len(self.mushrooms) == 0:
                    return WIN
                else:
                    return NORMAL
        return NORMAL

    def GetMole(self, x, y):
        for mole in self.moles:
            if mole.x == x and mole.y == y:
                return mole
        return None

    def createNewMap(self):
        self.placeObstacles()
        self.placeMushrooms()
        self.placeMoles()
        self.drawMap()

    def moveMole(self, mole, direction):
        mole.move(direction)
        return self.checkAndEat()

    def moveAllMoles(self):
        result = NORMAL
        for mole in self.moles:
            if self.distanceToTurtle(mole.x, mole.y) < mole.sniffRange:
                deltaX = self.turtle.x - mole.x
                deltaY = self.turtle.y - mole.y
                if abs(deltaX) > abs(deltaY):
                    if deltaX > 0:
                        direction = Right
                    else:
                        direction = Left
                else:
                    if deltaY > 0:
                        direction = Down
                    else:
                        direction = Up
            else:
                direction = randint(1, 4)
            if self.isMoleCanMove(mole, direction):
                result = self.moveMole(mole, direction)
                if result != NORMAL:
                    return result
        return result


    def formMap(self):
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                objectType = BackgroundIndex
                if self.isMole(x, y):
                    objectType = MoleIndex
                elif self.isTurtle(x, y):
                    objectType = TurtleIndex
                elif self.isMushroom(x, y):
                    objectType = MushroomIndex
                elif self.isObstacle(x, y):
                    objectType = ObstacleIndex

                self.placeObject(x, y, objectType)


    def InitMap(self):
        pass

    def placeObject(self, x, y, objectType):
        pass

    def drawMap(self):
        pass

    def tic(self):
        Result = self.moveAllMoles()
        self.drawMap()
        return Result