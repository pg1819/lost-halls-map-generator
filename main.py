import random
import sys

from map import Map
from tkinter import *


def create_room(canvas, x, y, room):
    if not room.empty:
        canvas.create_rectangle(x + 20, y + 20, x + 80, y + 80, fill="#C0C0C0", outline="#808080", width=3)

        if room.troom:
            canvas.create_text(x + 50, y + 50, text="troom", fill="#3282F6", font="Helvetica 10")
        if room.defender:
            canvas.create_text(x + 50, y + 50, text="defender", fill="#3282F6", font="Helvetica 10")
        if room.pot:
            canvas.create_text(x + 50, y + 50, text="pot", fill="#3282F6", font="Helvetica 10")
        if x == 400 and y == 400:
            canvas.create_text(x + 50, y + 50, text="spawn", fill="#3282F6", font="Helvetica 10")

        if room.up:
            canvas.create_rectangle(x + 40, y, x + 60, y + 20, fill="#808080", outline="#808080")
        if room.right:
            canvas.create_rectangle(x + 80, y + 40, x + 100, y + 60, fill="#808080", outline="#808080")
        if room.down:
            canvas.create_rectangle(x + 40, y + 80, x + 60, y + 100, fill="#808080", outline="#808080")
        if room.left:
            canvas.create_rectangle(x, y + 40, x + 20, y + 60, fill="#808080", outline="#808080")


if __name__ == "__main__":
    seed = random.randrange(sys.maxsize)
    print("Seed was:", seed)
    lh = Map(seed)

    root = Tk()
    root.title("Lost Halls")
    root.iconbitmap("./images/icon.ico")
    root.geometry("900x900")
    my_canvas = Canvas(root, width=900, height=900, bg="#000000")
    my_canvas.pack()
    for y in range(9):
        for x in range(9):
            create_room(my_canvas, x * 100, y * 100, lh.matrix[y][x])
    root.mainloop()
