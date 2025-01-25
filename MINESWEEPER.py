from tkinter import*
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.messagebox
import sys
import os
root=Tk()
root.title('Minesweeper Game')
w= root.winfo_screenwidth() 
h= root.winfo_screenheight()
root.geometry("%dx%d" % (w, h))
with open ('text.txt','w+') as f:
    a=''
    f.write(a)
def f1():
    os.system("level-final.py")
def f2():
    os.system("sign_in.py")


bg = PhotoImage(file = "title.png")
label1 = Label( root, image = bg)
label1.place(x = 0,y = 0)



photo=Image.open("sign.png")
resize1=photo.resize((200,100))
img1=ImageTk.PhotoImage(resize1)
btn1=tk.Button(root, image=img1,highlightthickness = 0, command=f2)
btn1.place(x=w-200*1.5,y=h-100*2.5)
#btn1.grid(row=0,column=0)

photo1=Image.open("play.png")
resize2=photo1.resize((200,100))
img2=ImageTk.PhotoImage(resize2)
btn2=tk.Button(root, image=img2,highlightthickness = 0, command=f1)
btn2.place(x=w/2-200/2,y=h-100*2.5)

#btn2.grid(row=2,column=1)



def onClick(): 
   tkinter.messagebox.showinfo("Instructions to play minesweeper","""
    Welcome to Minesweeper!

    The objective of Minesweeper is to clear the board without detonating any mines.
   
    How to Play:
    1. Left-click on a block to reveal what's underneath it.
    2. If you reveal a mine, you lose the game.
    3. If you reveal an empty space, it will show a number indicating how many mines are adjacent to that block.
    4. Use the numbers to deduce where the mines are located.
    5. Right-click on a block to flag it as a potential mine.
    6. Once you've flagged all the mines, you win the game!

    Advanced Strategies:
    - Pay attention to the numbers. They indicate how many mines are adjacent to a block.
    - Use logical deduction to determine the locations of mines.
    - Don't rush. Take your time to carefully consider each move.

    Good luck and have fun playing Minesweeper!
    """)  

photo2=Image.open("how.png")
resize3=photo2.resize((200,100))
img3=ImageTk.PhotoImage(resize3)
btn3=tk.Button(root, image=img3,highlightthickness = 0,command=onClick)
btn3.place(x=200/2,y=h-100*2.5)


  
root.mainloop()

    


    
