import os
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    print(Fore.CYAN + "="*50)
    print(Fore.GREEN + "        VIRTUAL OS MONITORING SYSTEM")
    print(Fore.CYAN + "="*50)

# ===== MAIN =====
while True:

    os.system("clear")
    banner()

    # 🔥 Check sudo
    if os.geteuid() != 0:
        print(Fore.RED + "⚠ Warning: Run with sudo for full functionality\n")

    print(Fore.YELLOW + "\nSelect a Module:\n")

    print(Fore.WHITE + "1. CPU Scheduling Simulator")
    print(Fore.WHITE + "2. System Resource Monitoring")
    print(Fore.WHITE + "3. Exit")

    choice = input(Fore.CYAN + "\nEnter your choice: ").strip()

    # ===== OPTION 1 =====
    if choice == "1":
        os.system("clear")
        print(Fore.MAGENTA + "\nLaunching CPU Scheduling Simulator...\n")

        # 👉 adjust path if needed
        import subprocess
        subprocess.run(["./scheduler"], cwd="C_Code")

        input(Fore.YELLOW + "\nPress Enter to return to dashboard...")

    # ===== OPTION 2 =====
    elif choice == "2":
        os.system("clear")
        print(Fore.MAGENTA + "\nLaunching System Monitoring...\n")

        print(Fore.YELLOW + "⚠ This requires sudo for full features")
        print("👉 You may be asked for password\n")

        # 🔥 IMPORTANT FIX (SUDO)
        os.system("sudo python3 Python_Code/monitor.py")

        input(Fore.YELLOW + "\nPress Enter to return to dashboard...")

    # ===== EXIT =====
    elif choice == "3":
        print(Fore.RED + "\nExiting Dashboard...\n")
        break

    else:
        print(Fore.RED + "\nInvalid choice!")
        input("Press Enter to continue...")
