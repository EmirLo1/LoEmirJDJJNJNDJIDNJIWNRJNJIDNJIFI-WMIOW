import os
import sys
import time
import subprocess
import threading


# =============================================================
# 1. Small "virus installing / downloading" tab window
#    Green hacker look, ~600x420, NOT fullscreen, stays on top
#    so the green cmd window is visible behind it.
#    100% cosmetic - no file deletion, no registry, no network.
# =============================================================
INSTALLER_SOURCE = r'''
import tkinter as tk
import random
import threading
import time

class InstallerScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VIRUS INSTALLER")
        self.root.configure(bg="black")
        self.root.geometry("620x440+80+80")   # small tab, top-left area
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        self.root.overrideredirect(False)      # keep title bar so it looks like a real tab

        # Title bar styling hint (works on most Windows 10/11 builds)
        try:
            self.root.wm_attributes("-alpha", 1.0)
        except Exception:
            pass

        frame = tk.Frame(self.root, bg="black",
                         highlightbackground="lime", highlightthickness=2)
        frame.pack(fill="both", expand=True)

        # Header
        header = tk.Label(frame, text="  VIRUS INSTALLER  v4.2.1  ",
                          font=("Courier New", 14, "bold"),
                          fg="black", bg="lime")
        header.pack(fill="x")

        # ASCII skull banner (compact)
        skull = (
            "   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄\n"
            " ▄█████████████████████████▄\n"
            "████████▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀████████\n"
            "███████  ▄▄▄▄▄     ▄▄▄▄▄  ███████\n"
            "███████  █████     █████  ███████\n"
            "███████  ▀▀▀▀▀     ▀▀▀▀▀  ███████\n"
            "████████▄               ▄████████\n"
            " ▀████████▄  ▄▄▄▄▄▄▄  ▄████████▀\n"
            "   ▀▀▀█████████████████████▀▀▀\n"
            "          ███       ███\n"
        )
        tk.Label(frame, text=skull, font=("Courier New", 8, "bold"),
                 fg="red", bg="black", justify="left").pack(pady=(6, 2))

        tk.Label(frame, text="⚠  INSTALLING VIRUS PAYLOAD  ⚠",
                 font=("Courier New", 14, "bold"),
                 fg="red", bg="black").pack(pady=2)

        tk.Label(frame, text="Do NOT close this window. Do NOT shut down your PC.",
                 font=("Courier New", 9),
                 fg="yellow", bg="black").pack(pady=2)

        # Blocky progress bar
        self.bar_canvas = tk.Canvas(frame, width=560, height=22,
                                    bg="black", highlightthickness=1,
                                    highlightbackground="lime")
        self.bar_canvas.pack(pady=6)
        self.bar_blocks = []
        for i in range(56):
            r = self.bar_canvas.create_rectangle(
                i * 10 + 1, 1, i * 10 + 9, 21,
                fill="black", outline="")
            self.bar_blocks.append(r)

        self.pct_label = tk.Label(frame, text="0%",
                                  font=("Courier New", 12, "bold"),
                                  fg="lime", bg="black")
        self.pct_label.pack()

        # Log box (compact)
        self.log = tk.Text(frame, height=8, width=74,
                           bg="black", fg="lime",
                           font=("Courier New", 9),
                           bd=0, highlightthickness=0)
        self.log.pack(pady=4)

        # Status line
        self.status = tk.Label(frame, text="> Initializing infection vector...",
                               font=("Courier New", 9, "bold"),
                               fg="lime", bg="black", anchor="w")
        self.status.pack(fill="x", padx=6, pady=(0, 6))

        # State
        self.progress = 0
        self.start_time = time.time()

        # Auto-close after ~6 seconds and hand off to the fake virus
        self.root.after(6000, self.close)

        # Threads
        threading.Thread(target=self.update_progress, daemon=True).start()
        threading.Thread(target=self.spam_log, daemon=True).start()
        threading.Thread(target=self.update_status, daemon=True).start()

        self.root.mainloop()

    def update_progress(self):
        while self.progress < 100:
            self.progress += random.randint(1, 3)
            if self.progress > 100:
                self.progress = 100
            filled = int(self.progress * 0.56)
            for i, r in enumerate(self.bar_blocks):
                self.bar_canvas.itemconfig(
                    r, fill="lime" if i < filled else "black")
            self.pct_label.config(text="{}%".format(self.progress))
            time.sleep(random.uniform(0.05, 0.15))

    def spam_log(self):
        actions = [
            "Downloading payload.bin from c2.evil.ru ...",
            "Injecting payload into svchost.exe (PID 1088)",
            "Disabling Windows Defender real-time protection",
            "Disabling UAC via registry hook",
            "Copying payload to C:\\Windows\\System32\\svchost32.dll",
            "Registering persistence key in HKLM\\...\\Run",
            "Deleting shadow copies via vssadmin",
            "Disabling system restore points",
            "Encrypting C:\\Users\\*\\Documents (AES-256)",
            "Encrypting C:\\Users\\*\\Pictures (AES-256)",
            "Overwriting MBR sector 0 with payload stub",
            "Corrupting recovery partition boot record",
            "Uploading encryption keys to C2 server",
            "Spawning 128 worker threads for encryption",
            "Clearing Windows event logs",
            "Deleting pagefile.sys and hiberfil.sys",
            "Installing rootkit driver rtcore64.sys",
            "Hooking kernel SSDT table",
            "Bypassing Secure Boot checks",
            "Finalizing infection... do not power off",
        ]
        while True:
            line = random.choice(actions)
            hx = "".join(random.choices("0123456789ABCDEF", k=8))
            ts = time.strftime("%H:%M:%S")
            self.log.insert(tk.END, "[{}][0x{}] {}\n".format(ts, hx, line))
            self.log.see(tk.END)
            if int(self.log.index("end-1c").split(".")[0]) > 200:
                self.log.delete("1.0", "2.0")
            time.sleep(random.uniform(0.04, 0.18))

    def update_status(self):
        lines = [
            "> Initializing infection vector...",
            "> Establishing C2 connection...",
            "> Downloading payload modules...",
            "> Bypassing antivirus heuristics...",
            "> Escalating privileges...",
            "> Injecting into system processes...",
            "> Encrypting user data...",
            "> Overwriting boot sector...",
            "> Covering tracks...",
            "> Infection complete. Rebooting in 10...",
        ]
        i = 0
        while True:
            self.status.config(text=lines[i % len(lines)])
            i += 1
            time.sleep(0.6)

    def close(self):
        try:
            self.root.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    InstallerScreen()
'''


# =============================================================
# 2. Fake virus fullscreen GUI (your provided script, unchanged)
# =============================================================
FAKE_VIRUS_SOURCE = r'''
import tkinter as tk
import random
import string
import threading
import time
import sys
import ctypes

class FakeVirusScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SYSTEM INFECTED")
        self.root.configure(bg='black')
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.root.bind('<Escape>', self.disable_event)
        self.root.bind('<Alt-F4>', self.disable_event)
        self.root.bind('<F4>', self.disable_event)
        self.root.overrideredirect(True)

        try:
            ctypes.windll.user32.BlockInput(True)
        except:
            pass

        frame = tk.Frame(self.root, bg='black')
        frame.pack(expand=True, fill='both')

        skull = tk.Label(frame, text="\u2620", font=('Arial', 200, 'bold'),
                         fg='red', bg='black')
        skull.pack(pady=(50, 0))

        title = tk.Label(frame, text="YOUR SYSTEM HAS BEEN INFECTED",
                         font=('Courier New', 36, 'bold'),
                         fg='red', bg='black')
        title.pack(pady=20)

        message = tk.Label(
            frame,
            text="All your files have been encrypted.\n"
                 "System32 is being deleted...\n"
                 "Registry is being corrupted...\n"
                 "Boot files are being destroyed...\n\n"
                 "Send 5 BTC to: 1A2B3C4D5E6F7G8H9I0J\n"
                 "or your computer will be destroyed forever.",
            font=('Courier New', 18), fg='lime', bg='black',
            justify='center')
        message.pack(pady=30)

        self.progress_canvas = tk.Canvas(
            frame, width=800, height=40, bg='black',
            highlightthickness=2, highlightbackground='red')
        self.progress_canvas.pack(pady=20)
        self.progress_bar = self.progress_canvas.create_rectangle(
            0, 0, 0, 40, fill='red', outline='')

        self.log = tk.Text(frame, height=8, width=100, bg='black',
                           fg='lime', font=('Courier New', 12),
                           bd=0, highlightthickness=0)
        self.log.pack(pady=10)

        self.counter_label = tk.Label(frame, text="Files deleted: 0",
                                      font=('Courier New', 20, 'bold'),
                                      fg='red', bg='black')
        self.counter_label.pack(pady=10)

        self.blink = True
        self.blink_label = tk.Label(
            frame, text="\u26a0 DO NOT TURN OFF YOUR COMPUTER \u26a0",
            font=('Courier New', 24, 'bold'),
            fg='yellow', bg='black')
        self.blink_label.pack(pady=20)

        self.files_deleted = 0
        self.progress = 0

        threading.Thread(target=self.update_progress, daemon=True).start()
        threading.Thread(target=self.update_counter, daemon=True).start()
        threading.Thread(target=self.blink_text, daemon=True).start()
        threading.Thread(target=self.spam_log, daemon=True).start()
        threading.Thread(target=self.random_move, daemon=True).start()

        self.root.mainloop()

    def disable_event(self, event=None):
        return "break"

    def update_progress(self):
        while True:
            self.progress += random.randint(1, 5)
            if self.progress > 100:
                self.progress = 0
            width = (self.progress / 100) * 800
            self.progress_canvas.coords(self.progress_bar, 0, 0, width, 40)
            time.sleep(0.1)

    def update_counter(self):
        while True:
            self.files_deleted += random.randint(100, 5000)
            self.counter_label.config(
                text="Files deleted: {:,}".format(self.files_deleted))
            time.sleep(0.3)

    def blink_text(self):
        while True:
            if self.blink:
                self.blink_label.config(fg='yellow')
            else:
                self.blink_label.config(fg='black')
            self.blink = not self.blink
            time.sleep(0.5)

    def spam_log(self):
        actions = [
            "Deleting C:\\Windows\\System32\\kernel32.dll",
            "Deleting C:\\Windows\\System32\\ntdll.dll",
            "Deleting C:\\Windows\\System32\\user32.dll",
            "Corrupting registry hive HKLM\\SYSTEM",
            "Corrupting registry hive HKLM\\SAM",
            "Encrypting C:\\Users\\Documents",
            "Encrypting C:\\Users\\Pictures",
            "Uploading data to 192.168.1.666",
            "Wiping MBR sector 0",
            "Disabling Windows Defender...",
            "Injecting payload into svchost.exe",
            "Bypassing UAC protections...",
            "Overwriting boot configuration...",
            "Destroying recovery partition...",
            "Deleting shadow copies...",
            "Formatting C:\\ drive...",
            "Sending encryption keys to C2 server...",
            "Deleting pagefile.sys",
            "Corrupting BIOS firmware...",
            "Disabling system restore points...",
        ]
        while True:
            line = random.choice(actions)
            hex_suffix = ''.join(random.choices('0123456789ABCDEF', k=8))
            self.log.insert(tk.END, "[0x{}] {}\n".format(hex_suffix, line))
            self.log.see(tk.END)
            if int(self.log.index('end-1c').split('.')[0]) > 100:
                self.log.delete('1.0', '2.0')
            time.sleep(random.uniform(0.05, 0.2))

    def random_move(self):
        while True:
            time.sleep(random.uniform(3, 8))
            try:
                self.root.attributes('-alpha', random.uniform(0.7, 1.0))
                time.sleep(0.05)
                self.root.attributes('-alpha', 1.0)
            except:
                pass


if __name__ == "__main__":
    FakeVirusScreen()
'''


# =============================================================
# Helpers
# =============================================================
def write_files():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_dir = os.getcwd()
    if not base_dir or not os.path.isdir(base_dir):
        base_dir = os.getcwd()

    installer_path = os.path.join(base_dir, "_installer_screen.py")
    virus_path = os.path.join(base_dir, "_fakevirus_payload.py")

    with open(installer_path, "w", encoding="utf-8") as f:
        f.write(INSTALLER_SOURCE)
    with open(virus_path, "w", encoding="utf-8") as f:
        f.write(FAKE_VIRUS_SOURCE)

    return installer_path, virus_path


def pick_python():
    py = sys.executable or "python"
    py_dir = os.path.dirname(py)
    pyw = os.path.join(py_dir, "pythonw.exe")
    if os.path.isfile(pyw):
        return pyw
    return py


def launch_dir_scan():
    # /k keeps window open, color 2 = green, dir /s = read-only recursive listing
    cmd = ('start "SYSTEM SCAN" cmd /k '
           '"color 2 && dir /s C:\\ && '
           'echo. && echo === SCAN COMPLETE === && '
           'echo LAUNCHING PAYLOAD... && '
           'timeout /t 3 /nobreak"')
    subprocess.Popen(cmd, shell=True)


def launch_installer(path):
    """Small top-most 'virus installing' tab window."""
    py = pick_python()
    flags = 0
    if os.name == "nt":
        flags = 0x00000008  # DETACHED_PROCESS
    subprocess.Popen([py, path], creationflags=flags, close_fds=True)


def launch_fake_virus(path, delay=6):
    """Wait for the installer tab to finish, then show fullscreen lockdown."""
    time.sleep(delay)
    py = pick_python()
    flags = 0
    if os.name == "nt":
        flags = 0x00000008
    subprocess.Popen([py, path], creationflags=flags, close_fds=True)


# =============================================================
# Orchestrate
# =============================================================
if __name__ == "__main__":
    print("[EmirLo] Writing payload files...")
    installer_path, virus_path = write_files()
    print("[EmirLo] Installer: {}".format(installer_path))
    print("[EmirLo] Virus    : {}".format(virus_path))

    # 1. Green cmd window: dir /s C:\ (visible in background)
    print("[EmirLo] Launching green dir /s scan...")
    launch_dir_scan()

    # 2. Small top-most "virus installing" tab (cmd still visible behind it)
    print("[EmirLo] Launching 'virus installing' tab...")
    launch_installer(installer_path)

    # 3. After the tab finishes (~6s), swap in the fullscreen fake virus
    print("[EmirLo] Fake virus will appear in 6 seconds...")
    t = threading.Thread(target=launch_fake_virus,
                         args=(virus_path, 6), daemon=True)
    t.start()

    time.sleep(8)
    print("[EmirLo] Done. Installer tab closed, fake virus is now on screen.")
