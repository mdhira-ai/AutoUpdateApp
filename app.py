import tkinter as tk
from version import *
from mylib.updatecheck import *


# Simple Tkinter GUI Window
root = tk.Tk()
root.title("Auto-Update App by Habib")
root.geometry("300x150")

label = tk.Label(root, text=f"Current Version: {CURRENT_VERSION}", font=("Arial", 12))
label.pack(pady=20)

label2 = tk.Label(root,text="hello world, md")
label2.pack()

btn = tk.Button(root, text="Check for Updates", command=check_for_updates)
btn.pack(pady=10)

root.mainloop()
