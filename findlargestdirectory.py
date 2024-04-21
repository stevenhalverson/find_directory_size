import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
import subprocess

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def select_directory():
    folder_selected = filedialog.askdirectory()
    directory.set(folder_selected)

def calculate_sizes():
    start_path = directory.get()
    sizes = {os.path.join(start_path, dir): get_size(os.path.join(start_path, dir)) for dir in os.listdir(start_path) if os.path.isdir(os.path.join(start_path, dir))}
    largest_dirs = sorted(sizes.items(), key=lambda x: x[1], reverse=True)
    for i in range(10):
        result.insert(tk.END, f"Directory: {largest_dirs[i][0]}, Size: {largest_dirs[i][1]} bytes")

def start_thread():
    threading.Thread(target=calculate_sizes).start()

def open_directory(event):
    selected_dir = result.get(result.curselection())
    # extract the directory path from the string
    dir_path = selected_dir.split("Directory: ")[1].split(", Size:")[0]
    subprocess.Popen(f'explorer "{dir_path}"')

root = tk.Tk()

directory = tk.StringVar()

frame1 = ttk.Frame(root)
frame1.pack()

frame2 = ttk.Frame(root)
frame2.pack()

label = ttk.Label(frame1, text="Select Directory")
label.pack(side="left")

entry = ttk.Entry(frame1, textvariable=directory)
entry.pack(side="left")

button = ttk.Button(frame1, text="Browse", command=select_directory)
button.pack(side="left")

calculate_button = ttk.Button(frame2, text="Calculate Sizes", command=start_thread)
calculate_button.pack()

result = tk.Listbox(root, width=100)
result.pack()
result.bind('<Double-1>', open_directory)

root.mainloop()
