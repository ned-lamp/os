# simple_tk_ui_basic.py
# A simple Tkinter UI using functions (no classes)

import tkinter as tk
from tkinter import ttk, messagebox

# --- Globals ---
root = tk.Tk()
root.title("Simple Tk UI")
root.geometry("420x300")

name_var = tk.StringVar()
age_var = tk.StringVar()
status_var = tk.StringVar(value="Ready")

# --- Functions ---
def add_person():
    name = name_var.get().strip()
    age = age_var.get().strip()

    if not name:
        messagebox.showwarning("Input Error", "Please enter a name.")
        return
    if age and not age.isdigit():
        messagebox.showwarning("Input Error", "Age must be a number.")
        return

    entry = f"{name} ({age})" if age else name
    listbox.insert(tk.END, entry)
    name_var.set("")
    age_var.set("")
    status_var.set(f"Added: {entry}")

def delete_person():
    sel = listbox.curselection()
    if not sel:
        messagebox.showinfo("Delete", "No item selected.")
        return
    item = listbox.get(sel[0])
    listbox.delete(sel[0])
    status_var.set(f"Deleted: {item}")

def clear_inputs():
    name_var.set("")
    age_var.set("")
    status_var.set("Inputs cleared")

def export_list():
    items = listbox.get(0, tk.END)
    if not items:
        messagebox.showinfo("Export", "Nothing to export.")
        return
    with open("people.txt", "w", encoding="utf-8") as f:
        for item in items:
            f.write(item + "\n")
    messagebox.showinfo("Export", "Saved to people.txt")
    status_var.set("Exported list to people.txt")

def show_about():
    messagebox.showinfo("About", "Simple Tk UI\nMade with ❤️ in Python")

# --- Menu Bar ---
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="Export", command=export_list)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menu_bar, tearoff=False)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menu_bar)

# --- Layout ---
frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w")
ttk.Entry(frame, textvariable=name_var, width=25).grid(row=0, column=1, pady=3)

ttk.Label(frame, text="Age:").grid(row=1, column=0, sticky="w")
ttk.Entry(frame, textvariable=age_var, width=25).grid(row=1, column=1, pady=3)

ttk.Button(frame, text="Add", command=add_person).grid(row=2, column=0, pady=6, sticky="w")
ttk.Button(frame, text="Clear", command=clear_inputs).grid(row=2, column=1, pady=6, sticky="e")

ttk.Label(frame, text="People List:").grid(row=3, column=0, sticky="w", pady=(10,0))
listbox = tk.Listbox(frame, height=8, width=40)
listbox.grid(row=4, column=0, columnspan=2, pady=4)

ttk.Button(frame, text="Delete Selected", command=delete_person).grid(row=5, column=0, columnspan=2, pady=6)

# --- Status bar ---
ttk.Label(root, textvariable=status_var, relief="sunken", anchor="w").pack(side="bottom", fill="x")

# --- Run the app ---
root.mainloop()
