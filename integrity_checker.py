import hashlib, os, json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


class FileIntegrityChecker:
    def __init__(self):
        self.file = "reference_hashes.json"
        try:
            with open(self.file) as f:
                self.refs = json.load(f)
        except:
            self.refs = {}

    def hash(self, path):
        try:
            h = hashlib.sha256()
            with open(path, "rb") as f:
                for data in iter(lambda: f.read(65536), b""):
                    h.update(data)
            return h.hexdigest()
        except:
            return None

    def store(self, path):
        h = self.hash(path)
        if not h:
            return False
        self.refs[path] = h
        with open(self.file, "w") as f:
            json.dump(self.refs, f, indent=4)
        return True

    def verify(self, path):
        if path not in self.refs:
            return None
        return self.hash(path) == self.refs[path]


class App:
    BG = "#F4F7FB"
    CARD = "#FFFFFF"
    BLUE = "#2563EB"
    TEXT = "#172033"
    GRAY = "#64748B"
    GREEN = "#16A34A"
    ORANGE = "#D97706"
    RED = "#DC2626"

    def __init__(self, root):
        self.root = root
        root.title("File Integrity Checker")
        root.geometry("820x620")
        root.minsize(760, 580)
        root.configure(bg=self.BG)

        self.checker = FileIntegrityChecker()
        self.selected = None
        self.build()

    def card(self, parent):
        outer = tk.Frame(parent, bg="#E2E8F0")
        inner = tk.Frame(outer, bg=self.CARD)
        inner.pack(padx=1, pady=1, fill="both", expand=True)
        return outer, inner

    def status(self, text, color=None):
        color = color or self.BLUE
        self.dot.config(bg=color)
        self.stat.config(text=text, fg=color)

    def build(self):
        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill="both", expand=True, padx=45, pady=25)

        # Header
        head = tk.Frame(main, bg=self.BG)
        head.pack(fill="x", pady=(0, 18))

        tk.Label(head, text="✓", font=("Segoe UI", 24, "bold"),
                 fg="white", bg=self.BLUE, width=2).pack(
                     side="left", padx=(0, 15))

        title = tk.Frame(head, bg=self.BG)
        title.pack(side="left")

        tk.Label(title, text="File Integrity Checker",
                 font=("Segoe UI", 24, "bold"),
                 fg=self.TEXT, bg=self.BG).pack(anchor="w")

        tk.Label(title, text="SHA-256 based file integrity verification",
                 font=("Segoe UI", 10), fg=self.GRAY,
                 bg=self.BG).pack(anchor="w")

        # File card
        o, c = self.card(main)
        o.pack(fill="x", pady=(0, 10))

        tk.Label(c, text="FILE SELECTION",
                 font=("Segoe UI", 9, "bold"),
                 fg=self.GRAY, bg=self.CARD).pack(
                     anchor="w", padx=25, pady=(12, 5))

        self.file_label = tk.Label(
            c, text="No file selected",
            font=("Segoe UI", 11), fg=self.GRAY,
            bg=self.CARD, anchor="w", wraplength=650)

        self.file_label.pack(fill="x", padx=25, pady=(0, 8))

        ttk.Button(c, text="  Select File  ",
                   command=self.select).pack(
                       anchor="w", padx=25, pady=(0, 12))

        # Hash card
        o, c = self.card(main)
        o.pack(fill="x", pady=(0, 10))

        tk.Label(c, text="SHA-256 HASH",
                 font=("Segoe UI", 9, "bold"),
                 fg=self.GRAY, bg=self.CARD).pack(
                     anchor="w", padx=25, pady=(12, 5))

        self.hash_label = tk.Label(
            c, text="Hash will appear here after selecting a file",
            font=("Consolas", 10), fg=self.GRAY,
            bg="#F8FAFC", anchor="w", wraplength=700,
            padx=15, pady=8)

        self.hash_label.pack(fill="x", padx=25, pady=(0, 12))

        # Buttons
        buttons = tk.Frame(main, bg=self.BG)
        buttons.pack(fill="x", pady=(0, 10))

        ttk.Button(buttons, text="Store Reference",
                   command=self.store).pack(side="left", padx=(0, 10))

        ttk.Button(buttons, text="Check Integrity",
                   command=self.check).pack(side="left")

        # Status
        o, c = self.card(main)
        o.pack(fill="x", pady=(0, 8))

        s = tk.Frame(c, bg=self.CARD)
        s.pack(fill="x", padx=25, pady=12)

        self.dot = tk.Label(s, text="", width=2, bg=self.BLUE)
        self.dot.pack(side="left", padx=(0, 12))

        self.stat = tk.Label(
            s, text="Ready — select a file to begin",
            font=("Segoe UI", 11, "bold"),
            fg=self.BLUE, bg=self.CARD)

        self.stat.pack(side="left")

        tk.Label(
            main,
            text="SHA-256 • Local verification • No file contents uploaded",
            font=("Segoe UI", 9), fg="#94A3B8",
            bg=self.BG).pack(pady=(3, 0))

    def select(self):
        path = filedialog.askopenfilename(title="Select a file")

        if not path:
            return

        self.selected = path
        self.file_label.config(text=path, fg=self.TEXT)

        h = self.checker.hash(path)

        if h:
            self.hash_label.config(text=h, fg=self.TEXT)
            self.status("File selected — ready for verification")
        else:
            self.hash_label.config(
                text="Unable to calculate SHA-256 hash",
                fg=self.RED)
            self.status("Unable to read selected file", self.RED)

    def store(self):
        if not self.selected:
            messagebox.showwarning(
                "No File Selected",
                "Please select a file first.")
            return

        if self.checker.store(self.selected):
            self.status(
                "Reference hash stored successfully", self.GREEN)
            messagebox.showinfo(
                "Reference Stored",
                "The SHA-256 reference hash has been stored successfully.")
        else:
            self.status("Unable to store reference hash", self.RED)
            messagebox.showerror(
                "Error", "Unable to store the file hash.")

    def check(self):
        if not self.selected:
            messagebox.showwarning(
                "No File Selected",
                "Please select a file first.")
            return

        result = self.checker.verify(self.selected)

        if result is None:
            self.status(
                "No reference hash found for this file",
                self.ORANGE)
            messagebox.showwarning(
                "No Reference Found",
                "Store a reference hash for this file first.")

        elif result:
            self.status(
                "INTEGRITY VERIFIED — file has not been modified",
                self.GREEN)
            messagebox.showinfo(
                "Integrity Verified",
                "The file has not been modified since the reference hash was stored.")

        else:
            self.status(
                "FILE MODIFIED — integrity check failed",
                self.RED)
            messagebox.showwarning(
                "Integrity Check Failed",
                "The file's SHA-256 hash does not match the stored reference.")


root = tk.Tk()
App(root)
root.mainloop()

