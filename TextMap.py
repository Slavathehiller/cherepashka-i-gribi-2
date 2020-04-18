from map import*

class TextMapManager(MapManager):
    TurtleSymbol = chr(81)
    BackgroundSymbol = chr(9633)
    MushroomSymbol = chr(0xB7)
    ObstacleSymbol = chr(0xA1)
    MoleSymbol = chr(0x69)
    objectTypes = [BackgroundSymbol, TurtleSymbol, MushroomSymbol, ObstacleSymbol, MoleSymbol]

    def InitMap(self):
        self.Map = []
        for y in range(self.sizeY):
            Line = list()
            for x in range(self.sizeX):
                Line.append(' ')
            self.Map.append(Line)

    def placeObject(self, x, y, objectType):
        self.Map[y][x] = self.objectTypes[objectType]

    def drawMap(self):
        self.formMap()
        MapString = ""
        for Line in self.Map:
            for Symbol in Line:
                MapString = MapString + Symbol
            MapString += "\n"
        self.OutMap.config(text=MapString, font="Symbol 20")
        self.OutMap.pack()
