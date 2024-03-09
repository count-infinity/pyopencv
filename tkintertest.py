import tkinter as tk
from tkinter import ttk


root = tk.Tk()

ttk.Label(root, text="Hello, world", padding=(30,10)).pack()

def greet():
    print(f"Hello, {user_name.get() or 'World'}!")

name_lbl = ttk.Label(root, text="Name: ")
name_lbl.pack(side="left", padx=(0,10))
user_name = tk.StringVar()
name_entry = ttk.Entry(root, width=15, textvariable=user_name)
name_entry.pack(side="left")
name_entry.focus()


green_button = ttk.Button(root, text="Greet", command=greet)
green_button.pack(side="left", fill="y")

quit_button = ttk.Button(root, text="Quit", command=root.destroy)
quit_button.pack(side="left")

root.mainloop()