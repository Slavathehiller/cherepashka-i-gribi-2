from tkinter import*
from cherepashka import*
from map import*
from PILMap import PILMapManager
from TextMap import TextMapManager
from Options import *
from PIL import Image, ImageTk


window = Tk()
window.title("Черепашка и грибы 2")
window.geometry("800x600")
window.iconbitmap('turtle.ico')
mainmenu = Menu(window)
window.config(menu=mainmenu)
menuFile = Menu(mainmenu, tearoff=0)
menuFile.add_command(label="Выход", command=lambda: exit(0))

options = SimpleOptions()

turtle = Turtle()

GameMode = 1

mapper = None
VisualMap = None

def Newgame():
    global mapper, VisualMap, turtle, gameEnded
    gameEnded = False
    if VisualMap != None:
       VisualMap.destroy()

    turtle = Turtle()

    if GameMode == 0:
        VisualMap = Label(window)
        mapper = TextMapManager(VisualMap, turtle, options)
    else:
        VisualMap = Frame(window)
        mapper = PILMapManager(VisualMap, turtle, options)
    VisualMap.pack(fill=BOTH)
    mapper.createNewMap()
    mapper.drawMap()

menuGame = Menu(mainmenu, tearoff=0)
menuGame.add_command(label="Начать игру", command=Newgame)

menuAbout = Menu(mainmenu, tearoff=0)

mainmenu.add_cascade(label="Файл", menu=menuFile)
mainmenu.add_cascade(label="Игра", menu=menuGame)
mainmenu.add_cascade(label="?", menu=menuAbout)


def ShowError(ErrorText, vidget = None):
    ErrorWindow = Toplevel()
    ErrorWindow.title("ОШИБКА")
    ErrorWindow.geometry("300x60")
    Errorlabel = Label(ErrorWindow, text=ErrorText)
    Errorlabel.pack()
    ErrorButton = Button(ErrorWindow, text="Ok")
    ErrorButton.bind("<Button-1>", lambda event: ErrorWindow.destroy())
    ErrorButton.pack()
    if vidget != None:
        vidget.focus_set()


def OptionsOk(optionswindow, Y, X ,M, O, SM, SMV, GM):
    global options, GameMode
    cordY = 0
    cordX = 1
    obst = 2
    moles = 3
    mush = 4
    IntValues = []
    for vidget in [Y, X, O, SM, M]:
        try:
            IntValues.append(int(vidget.get()))
        except:
            ShowError("Некоректные данные", vidget)
            return
    if IntValues[cordY] > 30:
        ShowError("Высота поля должна быть не более 30 клеток", Y)
        return

    if IntValues[cordX] > 100:
        ShowError("Ширина поля должна быть не более 100 клеток", X)
        return

    defOC = IntValues[cordY] * IntValues[cordX] // 10
    if IntValues[obst] > defOC:
        ShowError("Количество препятствий должно быть не более " + str(defOC), O)
        return

    defSM = IntValues[cordY] * IntValues[cordX] // 10
    if IntValues[moles] > defSM:
        ShowError("Количество кротов должно быть не более " + str(defSM), SM)
        return

    defMC = IntValues[cordY] * IntValues[cordX] // 20
    if IntValues[mush] > defMC:
        ShowError("Количество грибов должно быть не более " + str(defMC), M)
        return
    if IntValues[mush] < 1:
        ShowError("Количество грибов должно быть больше 0 ", M)
        return
    options.SlowMoles = SMV.get()
    options.sizeY = IntValues[cordY]
    options.sizeX = IntValues[cordX]
    options.ObstacleCount = IntValues[obst]
    options.MushroomCount = IntValues[mush]
    options.MoleCount = IntValues[moles]
    GameMode = GM.get()
    optionswindow.destroy()


def SetOptions():
    sizeYVar = StringVar()
    sizeXVar = StringVar()
    MushroomVar = StringVar()
    ObstacleVar = StringVar()
    MoleVar = StringVar()
    SlowMolesVar = IntVar()
    GameModVar = IntVar()

    optionswindow = Toplevel(window)
    optionswindow.geometry("500x170")
    optionswindow.title("Настройки игры")
    sizeYlabel = Label(optionswindow, text="Высота поля: ")
    sizeYlabel.grid(row=0, column=0, sticky=W, padx=4, pady=2)
    sizeYentry = Entry(optionswindow, textvariable=sizeYVar)
    sizeYVar.set(options.sizeY)
    sizeYentry.grid(row=0, column=1, sticky=W, padx=4, pady=2)

    sizeXlabel = Label(optionswindow, text="Ширина поля: ")
    sizeXlabel.grid(row=1, column=0, sticky=W, padx=4, pady=2)
    sizeXentry = Entry(optionswindow, textvariable=sizeXVar)
    sizeXVar.set(options.sizeX)
    sizeXentry.grid(row=1, column=1, sticky=W, padx=4, pady=2)

    MushroomCountLabel = Label(optionswindow, text="Количество грибов: ")
    MushroomCountLabel.grid(row=2, column=0, sticky=W, padx=4, pady=2)
    MushroomCountentry = Entry(optionswindow, textvariable=MushroomVar)
    MushroomVar.set(options.MushroomCount)
    MushroomCountentry.grid(row=2, column=1, sticky=W, padx=4, pady=2)

    ObstacleCountLabel = Label(optionswindow, text="Количество препятствий: ")
    ObstacleCountLabel.grid(row=3, column=0, sticky=W, padx=4, pady=2)
    ObstacleCountEntry = Entry(optionswindow, textvariable=ObstacleVar)
    ObstacleVar.set(options.ObstacleCount)
    ObstacleCountEntry.grid(row=3, column=1, sticky=W, padx=4, pady=2)

    MoleCountLabel = Label(optionswindow, text="Количество саблезубых кротов: ")
    MoleCountLabel.grid(row=4, column=0, sticky=W, padx=4, pady=2)
    MoleCountEntry = Entry(optionswindow, textvariable=MoleVar)
    MoleVar.set(options.MoleCount)
    MoleCountEntry.grid(row=4, column=1, sticky=W, padx=4, pady=2)

    SlowMolesCheckButton = Checkbutton(optionswindow, text="Медленные кроты", variable=SlowMolesVar)
    SlowMolesVar.set(options.SlowMoles)
    SlowMolesCheckButton.grid(row=0, column=2, sticky=W, padx=4, pady=2)

    GameModeText = Radiobutton(optionswindow, text="Текстовый режим", value=0, variable=GameModVar)
    GameModeGraphic = Radiobutton(optionswindow, text="Графический режим", value=1, variable=GameModVar)
    GameModVar.set(GameMode)
    GameModeText.grid(row=2, column=2, sticky=W, padx=4, pady=2)
    GameModeGraphic.grid(row=3, column=2, sticky=W, padx=4, pady=2)

    OKbutton = Button(optionswindow, text="Ok", height=1, width=6)
    OKbutton.grid(row=5, column=0, sticky=E, padx=30)
    OKbutton.bind("<Button-1>", lambda event: OptionsOk(optionswindow, sizeYentry, sizeXentry, MushroomCountentry, ObstacleCountEntry, MoleCountEntry, SlowMolesVar, GameModVar))

    Cancelbutton = Button(optionswindow, text="Cancel", height=1, width=6)
    Cancelbutton.grid(row=5, column=1, sticky=W, padx=30)
    Cancelbutton.bind("<Button-1>", lambda event: optionswindow.destroy())

menuGame.add_command(label="Настройки", command=SetOptions)

winimage =  ImageTk.PhotoImage(Image.open('win.gif'))
loseimage =  ImageTk.PhotoImage(Image.open('lose.gif'))

gameEnded = False

def WinGame():
    global gameEnded
    gameEnded = True
    winGameWindow = Toplevel()
    winGameWindow.title("Победа")
    winGameWindow.geometry("300x280")
    winGameLabel = Label(winGameWindow, text="Вы победили!\nПройдено шагов: " + str(turtle.step))
    winGameLabel.pack()

    winGameLabelGraphic = Label(winGameWindow)
    winGameLabelGraphic.config(image=winimage)
    winGameLabelGraphic.pack()

    CloseButton = Button(winGameWindow, text="Закрыть")
    CloseButton.bind("<Button-1>", lambda event: winGameWindow.destroy())
    CloseButton.pack()
    winsound.PlaySound("yraa.wav", winsound.SND_ASYNC + winsound.SND_PURGE)

def LoseGame():
    global gameEnded
    gameEnded = True
    MushroomPicked = options.MushroomCount - len(mapper.mushrooms)
    loseGameWindow = Toplevel()
    loseGameWindow.title("Поражение")
    loseGameWindow.geometry("300x300")
    loseGameLabel = Label(loseGameWindow, text="Вы проиграли\nПройдено шагов: " + str(turtle.step))
    loseGameLabel.pack()
    MushroomLabel = Label(loseGameWindow, text="Собрано грибов: " + str(MushroomPicked))
    MushroomLabel.pack()
    loseGameLabelGraphic = Label(loseGameWindow)
    loseGameLabelGraphic.config(image=loseimage)
    loseGameLabelGraphic.pack()
    CloseButton = Button(loseGameWindow, text="Закрыть")
    CloseButton.bind("<Button-1>", lambda event: loseGameWindow.destroy())
    CloseButton.pack()
    winsound.PlaySound("aiaiai.wav", winsound.SND_ASYNC + winsound.SND_PURGE)

def CheckGameState(state):
    if state == WIN:
        WinGame()
    elif state == LOSE:
        LoseGame()


def TurtleMove(direction):
    if mapper.isTurtleCanMove(direction):
        turtle.move(direction)
        CheckGameState(mapper.checkAndEat())


def KeyPress(event):
    if gameEnded:
        return
    if event.keycode == 38:
        TurtleMove(Up)
    elif event.keycode == 37:
        TurtleMove(Left)
    elif event.keycode == 40:
        TurtleMove(Down)
    elif event.keycode == 39:
        TurtleMove(Right)
    if not gameEnded:
        CheckGameState(mapper.tic())


window.bind("<Key>", KeyPress)

window.mainloop()