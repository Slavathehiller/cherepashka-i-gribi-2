from map import*
from tkinter import*
from PIL import Image, ImageTk

class PILMapManager(MapManager):
    turtleLeftImage = None
    turtleRightImage = None
    grassImage = None
    mushroomImage = None
    moleRightImage = None
    moleLeftImage = None
    objectImages = []

    def __init__(self, vidget, turtle, molesNumber):
        MapManager.__init__(self, vidget, turtle, molesNumber)
        image = Image.open('turtle.gif')
        self.turtleRightImage = ImageTk.PhotoImage(image)
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        self.turtleLeftImage = ImageTk.PhotoImage(image)
        image = Image.open('grass.gif')
        self.grassImage = ImageTk.PhotoImage(image)
        image = Image.open('mushroom.gif')
        self.mushroomImage = ImageTk.PhotoImage(image)
        image = Image.open('tree.gif')
        self.treeImage = ImageTk.PhotoImage(image)
        image = Image.open('krot.gif')
        self.moleRightImage = ImageTk.PhotoImage(image)
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        self.moleLeftImage = ImageTk.PhotoImage(image)

        self.objectImages = [self.grassImage, self.turtleRightImage, self.mushroomImage, self.treeImage, self.moleRightImage]


    def InitMap(self):
        self.Map=[]
        for i in range(self.sizeY):
            Line = list()
            frame = Frame(self.OutMap)
            frame.pack(side=TOP)
            for j in range(self.sizeX):
                square = Label(frame)
                square.pack(side=LEFT)
                Line.append(square)
            self.Map.append(Line)

    def placeObject(self, x, y, objectType):
        nowimage = self.objectImages[objectType]
        if objectType == MoleIndex:
            mole = self.GetMole(x, y)
            if mole.orientation == Left:
                nowimage = self.moleLeftImage
            elif mole.orientation == Right:
                nowimage = self.moleRightImage

        if objectType == TurtleIndex:
            if self.turtle.orientation == Left:
                nowimage = self.turtleLeftImage
            elif self.turtle.orientation == Right:
                nowimage = self.turtleRightImage

        self.Map[y][x].config(image=nowimage)

    def drawMap(self):
        MapManager.formMap(self)


