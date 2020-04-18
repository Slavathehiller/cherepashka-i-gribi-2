from Consts import*

class Zver:
    x = 0
    y = 0
    step = 0
    name = ""
    orientation = Right
    def move(self, direction):
        if direction == Up:
            self.y = self.y - 1
        if direction == Left:
            self.x = self.x - 1
            self.orientation = direction
        if direction == Down:
            self.y = self.y + 1
        if direction == Right:
            self.x = self.x + 1
            self.orientation = direction
        self.step = self.step + 1
        print(self.name + " переходит в точку", self.x, self.y)