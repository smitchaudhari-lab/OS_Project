import psutil
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ===== MAIN WINDOW =====
root = tk.Tk()
root.title("Advanced OS Monitoring System")
root.geometry("1000x700")

# ===== GRAPH SETUP =====
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5,4))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

cpu_data = []
mem_data = []

# ===== TABLE =====
columns = ("PID","Name","CPU","Memory")

tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)

tree.pack(fill=tk.BOTH, expand=True)

# ===== FUNCTIONS =====
def update_data():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent

    cpu_data.append(cpu)
    mem_data.append(mem)

    if len(cpu_data) > 30:
        cpu_data.pop(0)
        mem_data.pop(0)

    # Graph update
    ax1.clear()
    ax2.clear()

    ax1.plot(cpu_data)
    ax1.set_title("CPU Usage")

    ax2.plot(mem_data)
    ax2.set_title("Memory Usage")

    canvas.draw()

    # Update process table
    for row in tree.get_children():
        tree.delete(row)

    processes = []
    for p in psutil.process_iter(['pid','name','cpu_percent','memory_percent']):
        try:
            processes.append(p.info)
        except:
            pass

    processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)

    for p in processes[:10]:
        tree.insert("", tk.END, values=(
            p['pid'],
            p['name'][:15],
            p['cpu_percent'],
            round(p['memory_percent'],2)
        ))

    root.after(1000, update_data)

# ===== KILL PROCESS =====
def kill_process():
    selected = tree.focus()
    if not selected:
        return

    pid = tree.item(selected)["values"][0]

    try:
        psutil.Process(pid).terminate()
        messagebox.showinfo("Success", "Process killed")
    except:
        messagebox.showerror("Error", "Failed to kill process")

# ===== CHANGE PRIORITY =====
def set_priority():
    selected = tree.focus()
    if not selected:
        return

    pid = tree.item(selected)["values"][0]

    try:
        proc = psutil.Process(pid)
        proc.nice(10)
        messagebox.showinfo("Success", "Priority set to Low")
    except:
        messagebox.showerror("Error", "Permission denied")

# ===== BUTTONS =====
frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="Kill Process", command=kill_process).pack(side=tk.LEFT, padx=10)
tk.Button(frame, text="Set Low Priority", command=set_priority).pack(side=tk.LEFT, padx=10)

# ===== START =====
update_data()
root.mainloop()
