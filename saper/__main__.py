''' This project is unfinished but still i'm proud what i've done here with my limited knowledge'''

import tkinter as tk
import PIL
from PIL import Image,ImageTk
import random
def making_button(path,x,y):
    def destroyin_and_makig_fields():
        i.destroy()      
        makig_fields(path,x,y)
    i = tk.Button(root, command = destroyin_and_makig_fields)
    i.config(width=6,height=3)
    i.place(x = x, y = y)

    shifting()  
            
def makig_fields(path,x,y):
    
    black_pic = Image.open(path)
    new_size = (50,50)
    black_pic = black_pic.resize(new_size)
    black_pic_tk = ImageTk.PhotoImage(black_pic)
    black_pic_label = tk.Label(root,image = black_pic_tk)
    black_pic_label.image = black_pic_tk
    black_pic_label.place(x = x, y = y)
    shifting()
                 
def shifting ():
    global x,y
    x+=50
    if x == 400:
        x = 0
        y +=50
        
def making_number(i_0): 
    if i_0 == 0 or i_0%8==0:
        list_of_numbers_1 = [i_0-8,i_0-7,i_0+1,i_0+8,i_0+9]
    elif (i_0+1)%8 == 0:
        list_of_numbers_1 = [i_0-9,i_0-8,i_0-1,i_0+7,i_0+8]
    else:
        list_of_numbers_1 = [i_0-9,i_0-8,i_0-7,i_0-1,i_0+1,i_0+7,i_0+8,i_0+9]
        
    list_of_numbers_new = []   
    for i in list_of_numbers_1:
        if i <= 63 and i >= 0 :
                list_of_numbers_new.append(i)
    return list_of_numbers_new

def game():
    for i in range(64):
        suma = 0
        path = "D:/python/projekty_wlasne/saper/white_pic.gif"

        if i not in list_of_bombs:
            for el in list_of_lists:
                if i in el:
                    suma+=1

        if suma == 1:
            path = "D:/python/projekty_wlasne/saper/cyfra_1_.gif"
        elif suma == 2:
            path = "D:/python/projekty_wlasne/saper/2.gif"
        elif suma == 3:
            path = "D:/python/projekty_wlasne/saper/3.gif"
        elif suma == 4:
            path = "D:/python/projekty_wlasne/saper/4.gif"
        elif suma == 5:
            path = "D:/python/projekty_wlasne/saper/5.gif"
        elif suma == 6:
            path = "D:/python/projekty_wlasne/saper/6.gif"
        if i in list_of_bombs:
            path = "D:/python/projekty_wlasne/saper/bomb.gif"
        making_button(path,x,y)

        

#coordinates
y = 100   
x = 0 
i_0 = 0

list_of_bombs = []
another_bomb = 0
while len(list_of_bombs)<=8:
    another_bomb = random.randint(0,64) # tu powinno byc (0,64)
    if another_bomb not in list_of_bombs:
        list_of_bombs.append(another_bomb) 
list_of_bombs.sort()

list_of_lists = list(map(making_number,list_of_bombs))
list_of_lists.sort()
root = tk.Tk(className='Saper')
root.geometry('400x500')


        
game()

root.mainloop()


    