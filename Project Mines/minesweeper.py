import os
import tkinter as tk
import random as r
from tkinter import filedialog, Text
from PIL import Image, ImageTk
from gameSprite import Square, Timer, FlagCount, Face
from event import EventManager

root = tk.Tk()
root.title("Minesweeper")
root.geometry("1280x720")
root.configure(bg="#93979e")


"""
task: Remake click so neighbouring empty squares are revealed when an empty square is clicked. 
task: Make the first click have no adjacent mines: (Remove mines in a 3x3 grid and place them elsewhere)
task: Make a reset button
task: Death (Unbind all actions, reveal all other squares)
ctask: when middle click/ left&right click reveal a 3x3 square around it (if remaining mines = 0 then reveal others)
task: Top bar: emoji 
task: top bar: timer(done)
task: top bar: flagCount (done)
task: menu
"""

# Create a frame for the grid
grid_frame = tk.Frame(root, bg="#93979e")
grid_frame.place(relx=0.5, rely=0.5, anchor="center")


xGrid = 30 #30x16 grid of Squares
yGrid = 16
m = EventManager(xGrid, yGrid)
grid = [[Square(grid_frame, x=j,y=i, event=m) for i in range(yGrid)] for j in range(xGrid)]
for column in range(yGrid):
    for row in range(xGrid):
        grid[row][column].grid(row=column, column=row, padx = 0, pady = 0)
m.initialiseMines()


for row in grid:
    for item in row:
        item.until_I_Can_Think_Of_Other_Solutions_This_Is_The_Only_Way()


root.bind("<F2>", m.resetSq)

timerFrame = tk.Frame(root, bg="#93979e")
timerFrame.place(relx= 1.0, rely = 0, anchor="ne")
timer = [Timer(timerFrame, e=m, multiplier=(10**i)) for i in range(3)]
for i, sprite in enumerate(timer): 
    sprite.grid(row=0, column=2-i, padx=0, pady=0)

flagFrame = tk.Frame(root, bg="#93979e")
flagFrame.place(relx= 0.0, rely = 0, anchor="nw")
flag = [FlagCount(flagFrame, event=m, m=(10**i)) for i in range(3)]
for i, sprite in enumerate(flag): 
    sprite.grid(row=0, column=2-i, padx=0, pady=0)

face = Face(root=root, e=m)
face.place(relx=0.5, rely=0, anchor="n")

 
root.mainloop()