import tkinter as tk
from tkinter import filedialog, scrolledtext
import os

class NXViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("NX Viewer PRO 📁👁️")

        self.files = []
        self.index = 0

        self.w = 1
        self.h = 1
        self.mode = ""
        self.pixels = []
        self.palette = {}
        self.info = {}

        # ================= CANVAS =================
        self.canvas = tk.Canvas(root, width=500, height=500, bg="black")
        self.canvas.pack()

        # ================= INFO PANEL =================
        self.info_box = tk.LabelFrame(root, text="INFO", padx=5, pady=5)
        self.info_box.pack(fill="x")

        self.info_text = tk.Label(self.info_box, text="No file loaded", justify="left")
        self.info_text.pack()

        # ================= BUTTONS =================
        bar = tk.Frame(root)
        bar.pack()

        tk.Button(bar, text="Open Folder", command=self.open_folder).pack(side="left")
        tk.Button(bar, text="Refresh", command=self.scan).pack(side="left")

        tk.Button(bar, text="◀", command=self.prev).pack(side="left")
        tk.Button(bar, text="▶", command=self.next).pack(side="left")

        tk.Button(bar, text="Show Code", command=self.show_code).pack(side="left")

        self.label = tk.Label(root, text="No folder")
        self.label.pack()

        self.code_win = None

    # ================= FOLDER =================
    def open_folder(self):
        self.folder = filedialog.askdirectory()
        self.scan()

    def scan(self):
        if not hasattr(self, "folder"):
            return

        self.files = [
            os.path.join(self.folder, f)
            for f in os.listdir(self.folder)
            if f.lower().endswith(".nx")
        ]

        self.files.sort()
        self.index = 0

        if self.files:
            self.load(self.files[0])

    # ================= NAV =================
    def prev(self):
        if not self.files:
            return
        self.index = (self.index - 1) % len(self.files)
        self.load(self.files[self.index])

    def next(self):
        if not self.files:
            return
        self.index = (self.index + 1) % len(self.files)
        self.load(self.files[self.index])

    # ================= PARSER =================
    def load(self, path):
        with open(path, "r") as f:
            txt = f.read()

        self.raw = txt  # para code viewer

        self.info = {}

        header, rest = txt.split("DATA:", 1)

        fmt = header.split("FORMAT:")[1].split(";")[0]
        size = header.split("SIZE:")[1].split(";")[0]

        self.w, self.h = map(int, size.strip("[]").split(","))
        self.mode = fmt

        # ================= INFO =================
        if "INFO:" in txt:
            info_part = txt.split("INFO:")[1].strip()
            if "(" in info_part:
                info_part = info_part.split("(",1)[1].split(")",1)[0]

                for item in info_part.split(";"):
                    if ":" in item:
                        k,v = item.split(":",1)
                        self.info[k] = v.strip('"')

        # ================= DATA =================
        self.pixels = []
        self.palette = {}

        if fmt == "RGB_HEX":
            for p in rest.replace("\n",";").split(";"):
                if p and "," in p:
                    r,g,b = p.split(",")
                    self.pixels.append((int(r,16),int(g,16),int(b,16)))

        elif fmt == "RGBA_HEX":
            for p in rest.replace("\n",";").split(";"):
                if p and "," in p:
                    r,g,b,a = p.split(",")
                    self.pixels.append((int(r,16),int(g,16),int(b,16),int(a,16)))

        else:  # INDEXED
            if "PALETTE:" in txt:
                pal = txt.split("PALETTE:")[1].split("DATA:")[0]
                for line in pal.split("\n"):
                    if ":" in line:
                        k,v = line.split(":",1)
                        self.palette[k.strip()] = tuple(map(int,v.strip(";").split(",")))

            for p in rest.replace("\n",";").split(";"):
                if p.strip():
                    self.pixels.append(p.strip())

        self.render()
        self.update_info_ui()

        self.label.config(
            text=f"{os.path.basename(path)} | {self.mode} ({self.index+1}/{len(self.files)})"
        )

    # ================= INFO UI =================
    def update_info_ui(self):
        if not self.info:
            self.info_text.config(text="No INFO block")
            return

        txt = "\n".join([f"{k}: {v}" for k,v in self.info.items()])
        self.info_text.config(text=txt)

    # ================= RENDER =================
    def render(self):
        self.canvas.delete("all")

        pix = max(2, min(25, 500 // max(self.w, self.h)))

        i = 0
        for y in range(self.h):
            for x in range(self.w):

                if i >= len(self.pixels):
                    continue

                v = self.pixels[i]

                if self.mode == "RGB_HEX":
                    r,g,b = v
                    col = f"#{r:02x}{g:02x}{b:02x}"

                elif self.mode == "RGBA_HEX":
                    r,g,b,a = v
                    a /= 255
                    col = f"#{int(r*a):02x}{int(g*a):02x}{int(b*a):02x}"

                else:
                    col = "#000000"
                    if str(v) in self.palette:
                        r,g,b = self.palette[str(v)]
                        col = f"#{r:02x}{g:02x}{b:02x}"

                self.canvas.create_rectangle(
                    x*pix, y*pix,
                    (x+1)*pix, (y+1)*pix,
                    fill=col,
                    outline=""
                )

                i += 1

    # ================= CODE VIEW =================
    def show_code(self):
        if self.code_win and tk.Toplevel.winfo_exists(self.code_win):
            return

        self.code_win = tk.Toplevel(self.root)
        self.code_win.title("NX RAW CODE 🧾")

        text = scrolledtext.ScrolledText(self.code_win, width=80, height=30)
        text.pack()
        text.insert("1.0", self.raw)
        text.config(state="disabled")


# ================= RUN =================
root = tk.Tk()
app = NXViewer(root)
root.mainloop()