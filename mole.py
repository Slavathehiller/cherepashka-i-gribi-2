from Consts import*
from zver import*

class Mole(Zver):
    name = "Крот"
    isSlow = False
    step = 0
    sniffRange = 4

    def move(self, direction):
        if not self.isSlow or self.step % 2 == 0:
            Zver.move(self, direction)
        else:
            print(self.name + " стоит на месте")