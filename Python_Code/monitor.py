import psutil
import time
import os
from datetime import datetime
import matplotlib.pyplot as plt
from colorama import Fore, Style, init
import sys
import termios
import tty

init(autoreset=True)

LOG_FILE = "system_log.txt"

cpu_history = []
mem_history = []

# -------- KEY --------
def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return key

# -------- LOADING --------
def loading(text="Loading"):
    for dots in range(3):
        print(f"\r{text}{'.'*(dots+1)}", end="", flush=True)
        time.sleep(0.4)
    print("\r" + " "*40, end="\r")

# -------- BAR --------
def bar(p):
    filled = int(p // 5)
    empty = 20 - filled

    if p < 40:
        color = Fore.GREEN
    elif p < 70:
        color = Fore.YELLOW
    else:
        color = Fore.RED

    return color + "█"*filled + Fore.WHITE + "░"*empty

# -------- LOG --------
def log(cpu, mem):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now()} CPU:{cpu}% MEM:{mem}%\n")
    except:
        pass

# -------- AI ANALYZER --------
def ai_analyzer(cpu_hist, mem_hist):
    print("\n" + Fore.CYAN + Style.BRIGHT + "="*40)
    print(Fore.CYAN + Style.BRIGHT + "        System Analysis Engine")
    print(Fore.CYAN + Style.BRIGHT + "="*40)

    if len(cpu_hist) < 3:
        print(Fore.YELLOW + "Collecting data...")
        return

    cpu_current = cpu_hist[-1]
    mem_current = mem_hist[-1]

    cpu_trend = cpu_hist[-1] - cpu_hist[0]
    mem_trend = mem_hist[-1] - mem_hist[0]

    # 🔥 Improved thresholds
    if cpu_current > 50 or mem_current > 60:
        state = "UNSTABLE"
        state_color = Fore.RED + Style.BRIGHT
    elif cpu_current > 30:
        state = "WARNING"
        state_color = Fore.YELLOW + Style.BRIGHT
    else:
        state = "STABLE"
        state_color = Fore.GREEN + Style.BRIGHT

    # 🧠 STATUS
    print("\n" + Fore.WHITE + "System State: " + state_color + state)

    # 🔍 INSIGHTS
    print(Fore.CYAN + "\nInsights:")
    if cpu_trend > 20:
        print(Fore.YELLOW + "⚠ CPU increasing rapidly")
    if mem_trend > 15:
        print(Fore.YELLOW + "⚠ Memory usage rising")
    if cpu_trend <= 20 and mem_trend <= 15:
        print(Fore.GREEN + "✔ Resource usage stable")

    # 💡 RECOMMENDATIONS
    print(Fore.MAGENTA + "\nRecommendation:")
    if cpu_current > 50:
        print(Fore.RED + "→ Close heavy CPU applications")
    if mem_current > 60:
        print(Fore.RED + "→ Free RAM / close background apps")
    if cpu_current <= 30 and mem_current <= 50:
        print(Fore.GREEN + "→ System running efficiently")

    # 🔮 PREDICTION
    print(Fore.BLUE + "\nPrediction:")
    if cpu_trend > 20 or mem_trend > 15:
        print(Fore.YELLOW + "→ System may lag soon")
    else:
        print(Fore.GREEN + "→ System stable")
# -------- UI --------
def box_line(text=""):
    print(f"│ {text:<44} │")

def header():
    print(Fore.CYAN + Style.BRIGHT + "┌" + "─"*46 + "┐")
    print(Fore.CYAN + Style.BRIGHT + "│" + " VIRTUAL OS MONITORING SYSTEM ".center(46) + "│")
    print(Fore.CYAN + Style.BRIGHT + "└" + "─"*46 + "┘")

def display(cpu, mem, processes):
    header()

    print(Fore.WHITE + " SYSTEM INFO ")
    print("┌" + "─"*46 + "┐")
    box_line(f"CPU Cores : {psutil.cpu_count()}")
    box_line(f"Memory    : {round(psutil.virtual_memory().total / (1024**3),2)} GB")
    print("└" + "─"*46 + "┘")

    print(Fore.YELLOW + "\n CPU ")
    print("┌" + "─"*46 + "┐")
    box_line(f"Usage : {bar(cpu)} {cpu:5.1f}%")
    print("└" + "─"*46 + "┘")

    print(Fore.BLUE + "\n MEMORY ")
    print("┌" + "─"*46 + "┐")
    box_line(f"Usage : {bar(mem)} {mem:5.1f}%")
    print("└" + "─"*46 + "┘")

    print(Fore.MAGENTA + "\n TOP PROCESSES ")
    print("┌" + "─"*46 + "┐")
    box_line("No   PID     Name       CPU%   MEM%")

    for i, p in enumerate(processes[:5]):
        name = p['name'][:10]
        line = f"{i+1:<3} {p['pid']:<7} {name:<10} {p['cpu_percent']:<6} {round(p['memory_percent'],2)}"
        if i == 0:
            print(Fore.RED + Style.BRIGHT + f"│ {line:<44} │")
        else:
            box_line(line)

    print("└" + "─"*46 + "┘")

# -------- GRAPH --------
def track_process(processes):
    try:
        print("\nSelect process (1-5):")
        for i, p in enumerate(processes[:5]):
            print(f"{i+1}. {p['name']} (PID {p['pid']})")

        choice = int(input("Enter choice: "))
        selected = processes[choice-1]
        proc = psutil.Process(selected['pid'])

        cpu_list = []
        mem_list = []

        plt.figure(selected['name'])

        while True:
            cpu = proc.cpu_percent(interval=1)
            mem = proc.memory_percent()

            cpu_list.append(cpu)
            mem_list.append(mem)

            if len(cpu_list) > 20:
                cpu_list.pop(0)
                mem_list.pop(0)

            plt.clf()

            plt.subplot(2,1,1)
            plt.plot(cpu_list)
            plt.title("CPU Usage (%)")

            plt.subplot(2,1,2)
            plt.plot(mem_list)
            plt.title("Memory Usage (%)")

            plt.tight_layout()
            plt.pause(0.3)

    except KeyboardInterrupt:
        plt.close()
        print("\nGraph stopped.")
        time.sleep(1)

# -------- MAIN --------
def monitor():
    while True:
        loading("Loading")
        os.system("clear")

        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent

        cpu_history.append(cpu)
        mem_history.append(mem)

        if len(cpu_history) > 5:
            cpu_history.pop(0)
            mem_history.pop(0)

        processes = []
        for p in psutil.process_iter(['pid','name','cpu_percent','memory_percent']):
            try:
                processes.append(p.info)
            except:
                pass

        processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)

        display(cpu, mem, processes)
        log(cpu, mem)

        print(Fore.CYAN + "\nAI analyzing system...")
        time.sleep(1)
        ai_analyzer(cpu_history, mem_history)

        print(Fore.CYAN + "\n┌" + "─"*46 + "┐")
        print(Fore.CYAN + "│ [1] Refresh  [2] Kill  [3] Priority │")
        print(Fore.CYAN + "│ [4] Graph    [5] Exit              │")
        print(Fore.CYAN + "└" + "─"*46 + "┘")

        print(Fore.YELLOW + "Press key: ", end="", flush=True)

        choice = get_key()

        if choice == "1":
            continue

        elif choice == "2":
            pid = input("\nEnter PID: ")
            try:
                psutil.Process(int(pid)).terminate()
                print("Process killed")
            except:
                print("Error")
            time.sleep(2)

        elif choice == "3":
            pid = input("\nEnter PID: ").strip()

            if not pid.isdigit():
                print("Invalid PID!")
                time.sleep(2)
                continue

            try:
                proc = psutil.Process(int(pid))
                current = proc.nice()

                print(f"\nCurrent Priority: {current}")
                print("Range: -20 (high) to 19 (low)")

                new = input("Enter new priority: ").strip()

                if not new.lstrip("-").isdigit():
                    print("Invalid input!")
                else:
                    new = int(new)
                    if -20 <= new <= 19:
                        proc.nice(new)
                        print("Priority updated successfully!")
                    else:
                        print("Out of range!")

            except psutil.AccessDenied:
                print("Permission denied! Run with sudo.")
            except psutil.NoSuchProcess:
                print("Process not found!")

            time.sleep(2)

        elif choice == "4":
            track_process(processes)

        elif choice == "5":
            break

        else:
            print("Invalid choice")
            time.sleep(2)

monitor()
