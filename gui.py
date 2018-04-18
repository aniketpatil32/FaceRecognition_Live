import Tkinter as tk
import os
import random

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
    
def train():
    os.system("python training.py")
    #root.destroy()
def recognition():
    os.system("python new_detector.py")
    #root.destroy()
def register():
    os.system("python registration.py")
    #root.destroy() 
root = tk.Tk()
# width x height + x_offset + y_offset:
#root=tk.Toplevel(root)
root.title("Home")
root.geometry("200x150")
center(root)
w = tk.Button(root, text="Train", bg="red", fg="white",command=train)
w.pack(fill=tk.X,padx=10,pady=10)
w = tk.Button(root, text="Recognition", bg="green", fg="black",command=recognition)
w.pack(fill=tk.X,padx=10,pady=10)
w = tk.Button(root, text="Register", bg="blue", fg="white",command=register)
w.pack(fill=tk.X,padx=10,pady=10)

root.mainloop()

