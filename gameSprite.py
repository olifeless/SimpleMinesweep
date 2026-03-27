import tkinter as tk
from PIL import Image, ImageTk
import random as r
from time import sleep
import threading

class Sprites(tk.Label):
    def  __init__(self, root, pImage):
        super().__init__(master=root, image = pImage, borderwidth=0)



class RedNum(Sprites):
    
    formatted = False
    sprite = {0: "sprites/sprite_00.png",
        1: "sprites/sprite_01.png",
        2: "sprites/sprite_02.png",
        3: "sprites/sprite_03.png",
        4: "sprites/sprite_04.png",
        5: "sprites/sprite_05.png",
        6: "sprites/sprite_06.png",
        7: "sprites/sprite_07.png",
        8: "sprites/sprite_08.png",
        9: "sprites/sprite_09.png",
        "-": "sprites/sprite_-.png",}
    

   
   
    def __init__(self, root):
        if not RedNum.formatted:
            for num in RedNum.sprite.keys():
                temp = Image.open(RedNum.sprite[num]).resize((32, 64), Image.NEAREST)
                temp = ImageTk.PhotoImage(temp)
                RedNum.sprite[num] = temp
            RedNum.formatted = True
        super().__init__(root=root, pImage =RedNum.sprite[0])
    
class Square(Sprites):
    UNREVEALED = 0 #Number of SAFE squares not revealed, game ends when it hits 0

    def __init__(self, root, x, y, event):
        self.__img = Image.open("sprites/blank.png").resize((32, 32), Image.NEAREST)
        self.__img = ImageTk.PhotoImage(self.__img)
        super().__init__(root, pImage=self.__img)
        self.__revealed = False #Is it revealed
        self.__mines = False #If it has a mine
        self.__flagged = False #Is it flagged
        self.__adjMines = 0 #How many mines around it
        self.__xCoord = x #i mean
        self.__yCoord = y #self explanatory
        self.__safe = False #if it is within "spawn" so no mines can be here
        self.__event = event #event manager
        self.__event.registerSq(self, x, y)
        Square.UNREVEALED += 1
        #If a new boolean/variable is added, remember to reset it in reset()

    def until_I_Can_Think_Of_Other_Solutions_This_Is_The_Only_Way(self):
        self.bind("<Button-1>", lambda e: self.__event.fixMines(e, self.__xCoord, self.__yCoord))


    def bindInput(self):
        self.unbind("<Button-1>")
        # self.bind("<ButtonPress>", lambda e: self.__event.onPressed(e,self.__xCoord, self.__yCoord))
        # self.bind("<ButtonRelease>", lambda e: self.__event.onReleased(e,self.__xCoord, self.__yCoord))
        self.bind("<Button-1>", self.clicked)
        self.bind("<Button-3>", self.flag)
        #Think of a way to get rid of the the fixMines bind
        
    def getState(self): return self.__revealed
    def getMines(self): return self.__mines
    def getAdjMines(self): return self.__adjMines
    def getFlagged(self): return self.__flagged
        
    def addAdjMines(self):
        self.__adjMines += 1

    def removeAdjMines(self):
        self.__adjMines -= 1

    
    def flag(self, event=0):
        if not self.__revealed:
            if not self.__flagged:
                self.__img = Image.open("sprites/flag.png").resize((32, 32), Image.NEAREST)
                self.__flagged = True
            elif self.__flagged:
                self.__img = Image.open("sprites/blank.png").resize((32, 32), Image.NEAREST)
                self.__flagged = False
            self.__event.broadcastFlag(self.__flagged)
            self.__img = ImageTk.PhotoImage(self.__img)
            self.config(image=self.__img)

    def removeMine(self):
        self.__mines = False
        self.__safe = True
        Square.UNREVEALED += 1

    def setMineState(self):
        if not self.__mines and not self.__safe:
            self.__mines = True
            Square.UNREVEALED -= 1
            return True
        return False

    def clicked(self, event=0):
        if not self.__flagged:
            if not self.__revealed:
                self.__revealed = True
                if self.__mines:
                    self.__img = Image.open("sprites/red_mine.png").resize((32, 32), Image.NEAREST)
                    self.__event.death()
                else:
                    Square.UNREVEALED -= 1
                    if not Square.UNREVEALED:
                        self.__event.completed()
                    match self.__adjMines:
                        case 0: 
                            self.__img = Image.open("sprites/0.png").resize((32, 32), Image.NEAREST)
                            self.__event.checkNeighbour(self.__xCoord, self.__yCoord)
                        case 1: self.__img = Image.open("sprites/1.png").resize((32, 32), Image.NEAREST)
                        case 2: self.__img = Image.open("sprites/2.png").resize((32, 32), Image.NEAREST)
                        case 3: self.__img = Image.open("sprites/3.png").resize((32, 32), Image.NEAREST)
                        case 4: self.__img = Image.open("sprites/4.png").resize((32, 32), Image.NEAREST)
                        case 5: self.__img = Image.open("sprites/5.png").resize((32, 32), Image.NEAREST)
                        case 6: self.__img = Image.open("sprites/6.png").resize((32, 32), Image.NEAREST)
                        case 7: self.__img = Image.open("sprites/7.png").resize((32, 32), Image.NEAREST)
                        case 8: self.__img = Image.open("sprites/8.png").resize((32, 32), Image.NEAREST)
                        case _: self.__img = Image.open("sprites/dead.png").resize((32, 32), Image.NEAREST)
                self.__img = ImageTk.PhotoImage(self.__img)
                self.config(image=self.__img)
            elif event != 0: #Revealed square AND triggered by actual mouse button clicking
                # Remove unessasary recursion by checking if this was executed by a previous stack.
                self.__event.scan(x=self.__xCoord, y=self.__yCoord, mines= self.__adjMines)
                
    
    def reset(self):
        self.__img = Image.open("sprites/blank.png").resize((32, 32), Image.NEAREST)
        self.__img = ImageTk.PhotoImage(self.__img)
        self.config(image=self.__img)
        if self.__revealed or self.__mines:
            self.__revealed = False
            Square.UNREVEALED += 1
            self.__mines = False
        self.__flagged = False
        self.__adjMines = 0
        self.__safe = False

    def gameOver(self):
        if not self.__revealed:
            if self.__mines^self.__flagged:
                if self.__mines:
                    self.__img = Image.open("sprites/mine.png").resize((32, 32), Image.NEAREST)
                elif self.__flagged:
                    self.__img = Image.open("sprites/wrong_mine.png").resize((32, 32), Image.NEAREST)
                self.__img = ImageTk.PhotoImage(self.__img)
                self.config(image=self.__img)
                self.__revealed = True
            else:
                self.clicked(0)
    
    
    def tempChange(self):
        if not self.__revealed and not self.__flagged:
            if self.__img != Image.open("sprites/0.png").resize((32,32), Image.NEAREST):
                self.__realImg = self.__img
                self.__img = Image.open("sprites/0.png").resize((32,32), Image.NEAREST)
            else:
                try:
                    self.__img = self.__realImg
                except:
                    pass
            self.__img = ImageTk.PhotoImage(self.__img)
            self.config(image=self.__img)
     #Check neighbour squares, if there are mines, add it to a variable. If that variable = self.__adjMines then reveal 3x3 square

        


class Timer(RedNum):
    time = 0 
    interupt = False

    def __init__(self, root, e, multiplier=int):
        super().__init__(root)
        self.__multiplier = multiplier #Since multiplier is a unique identifier, ill use it to label each sprite.
        self.__event = e
        e.addTimer(self)
        


    def startTime(self):
        #Solution, only one sprite runs this timer
        Timer.interupt = False
        while Timer.time < 999 and not Timer.interupt:
            Timer.time += 1
            self.__event.broadcastChangeSkin("t")
            sleep(1)


    def changeSkin(self):
            
        num = (Timer.time % (10 * self.__multiplier)) // self.__multiplier
        self.config(image = RedNum.sprite[num])


    def stop(self):
        Timer.interupt = True

    def restart(self):
        self.stop()
        Timer.time = 0
        self.config(image = RedNum.sprite[0])

    def startThread(self):
        thread = threading.Thread(target=self.startTime, daemon=True).start() #Thread for timer
        #Bonus if I can make it so not all 3 sprites have to update every time (eg, 012 to 013 only requires the last digit to update.)

class FlagCount(RedNum):
    remainMines = 99

    def __init__(self, root, event, m=int):
        super().__init__(root=root)
        self.__event = event
        event.addFlagCounter(self)
        self.__multiplier = m
        self.changeSkin()

    def changeSkin(self):
        if FlagCount.remainMines < 0:
            if self.__multiplier == 100:
                self.config(image=RedNum.sprite["-"])
                return
                
        num = (abs(FlagCount.remainMines) % (10 * self.__multiplier)) // self.__multiplier
        self.config(image = RedNum.sprite[num])


    def reset(self):
        FlagCount.remainMines = 99
        self.__event.broadcastChangeSkin("f")

    def flagged(self):
        FlagCount.remainMines -= 1
        self.__event.broadcastChangeSkin("f")

    def unflagged(self):
        FlagCount.remainMines += 1
        self.__event.broadcastChangeSkin("f")

class Face(Sprites):
    formatted = False
    faces = {"dead" : "sprites/dead.png",
             "smile" : "sprites/smile.png",
             "smile2": "sprites/smile_clicked.png",
             "sunglasses": "sprites/completed.png",
             "wow": "sprites/wow.png",
             }
    
    Img = None
        
    def __init__(self, root, e):
        if not Face.formatted:
            for spr in Face.faces.keys():
                temp = Image.open(Face.faces[spr]).resize((40, 40), Image.NEAREST)
                temp = ImageTk.PhotoImage(temp)
                Face.faces[spr] = temp
        super().__init__(root=root, pImage=Face.faces["smile"])
        Face.Img = Face.faces["smile"]
        self.__event = e
        e.addface(self)
        # self.config(cursor="mouse2")
        self.bind("<Button-1>", self.pressed)
        self.bind("<ButtonRelease-1>", self.released)
        

    def pressed(self, e):
        self.config(image = Face.faces["smile2"])

    def released(self, e):
        self.config(image= Face.faces["smile"])
        self.__event.resetSq(0)

    def wow(self): #might need a thread for this
        self.config(image= Face.faces["wow"])

    def completed(self):
        self.config(image= Face.faces["sunglasses"])

    def over(self):
        self.config(image= Face.faces["dead"])

    def reset(self):
        self.config(image = Face.faces["smile"])
