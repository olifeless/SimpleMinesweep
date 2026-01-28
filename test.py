import tkinter as tk
from gameSprite import Square
from PIL import Image, ImageTk



class Square(tk.Label):
    mouseClicked = set()

    def __init__(self, root, pImage, x, y):
        self.x = x
        self.y = y
        super().__init__(root, image=pImage, borderwidth=0, cursor="hand2")


    def clicked(self, e):
        Square.mouseClicked.add(e.num)
        if not self.checkIfBothMouseButtonsPressed():
            with open("runs.txt", "a") as f:
                f.write(f"Square at {self.x}, {self.y} has been clicked.\n")
            f.close()

    def released(self, e):
        Square.mouseClicked.remove(e.num)
        if not self.checkIfBothMouseButtonsPressed():
            with open("runs.txt", "a") as f:
                f.write(f"Square at {self.x}, {self.y} has been released.\n")
            f.close()



    def checkIfBothMouseButtonsPressed(self):
        if 1 in Square.mouseClicked and 3 in Square.mouseClicked:
            with open("runs.txt", "a") as f:
                f.write(f"Square at {self.x}, {self.y} has been left and right clicked.\n")
            f.close()
            return True
        return False

#Try to include binds for left+right click. Write the result in runs.txt

    

    def bindAll(self):
        self.bind("<ButtonPress-1>", self.clicked)
        self.bind("<ButtonRelease-1>", self.released)
        self.bind("<ButtonPress-3>", self.clicked)
        self.bind("<ButtonRelease-3>", self.released)

root = tk.Tk()
root.title("Square Click Test")


img = Image.open("sprites/blank.png").resize((32, 32), Image.NEAREST)
img = ImageTk.PhotoImage(img)
grid = [[Square(root, pImage=img, x=i, y=j)for i in range(3)] for j in range(3)] #Creates a grid of 3x3 squares

for column in range(3):
    for row in range(3):
        grid[row][column].bindAll()
        grid[row][column].grid(row=column, column=row, padx = 0, pady = 0) #Places the 3x3 squares in the root



f = open("runs.txt", "r")


with open("runs.txt", "a") as f:
    f.write(f"New Run\n")
f.close()




root.mainloop()