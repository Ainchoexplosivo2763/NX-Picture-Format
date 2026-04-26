import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

class NXLiveIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("NX Live IDE (Code Editor)")

        # ================= LAYOUT =================
        self.left = tk.Frame(root)
        self.left.pack(side="left", fill="both", expand=True)

        self.right = tk.Frame(root)
        self.right.pack(side="right", fill="y")

        # ================= CODE EDITOR =================
        self.code = scrolledtext.ScrolledText(self.left, width=70)
        self.code.pack(fill="both", expand=True)
        self.code.bind("<KeyRelease>", lambda e: self.update())

        # shortcuts
        self.code.bind("<Control-a>", lambda e: self.select_all())
        self.code.bind("<Control-c>", lambda e: self.copy())
        self.code.bind("<Control-v>", lambda e: self.paste())

        # ================= CANVAS =================
        self.canvas = tk.Canvas(self.right, width=420, height=420, bg="black")
        self.canvas.pack()

        # ================= INFO =================
        self.info_box = tk.LabelFrame(self.right, text="INFO", padx=5, pady=5)
        self.info_box.pack(fill="x")

        self.info_label = tk.Label(self.info_box, text="No INFO", justify="left")
        self.info_label.pack()

        # ================= ERROR =================
        self.err = tk.Label(self.right, text="OK", fg="green")
        self.err.pack()

        # ================= BUTTONS =================
        bar = tk.Frame(self.right)
        bar.pack()

        tk.Button(bar, text="Open", command=self.open_file).pack(side="left")
        tk.Button(bar, text="Save", command=self.save_file).pack(side="left")
        tk.Button(bar, text="Reset", command=self.load_sample).pack(side="left")

        tk.Button(bar, text="Select All", command=self.select_all).pack(side="left")
        tk.Button(bar, text="Copy", command=self.copy).pack(side="left")
        tk.Button(bar, text="Paste", command=self.paste).pack(side="left")

        # ================= SAMPLE =================
        self.load_sample()
        self.update()

    # =========================================================
    # SAMPLE
    # =========================================================
    def load_sample(self):
        self.code.delete("1.0", "end")
        self.code.insert("1.0",
"""NX
FORMAT:RGB_HEX;SIZE:[4,4];
DATA:
FF,00,00;00,FF,00;00,00,FF;FF,FF,FF;
FF,FF,FF;00,00,00;FF,00,FF;00,FF,FF;
FF,00,00;00,FF,00;00,00,FF;FF,FF,FF;
FF,FF,FF;00,00,00;FF,00,FF;00,FF,FF;

INFO:(TITLE:"Demo";AUTHOR:"NemKazi";STYLE:"Pixel";)
""")

    # =========================================================
    # FILE I/O
    # =========================================================
    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("NX","*.nx")])
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            self.code.delete("1.0", "end")
            self.code.insert("1.0", f.read())
        self.update()

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".nx")
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.code.get("1.0", "end"))
        messagebox.showinfo("NX", "Saved!")

    # =========================================================
    # CLIPBOARD
    # =========================================================
    def select_all(self):
        self.code.tag_add("sel", "1.0", "end")

    def copy(self):
        try:
            text = self.code.get("sel.first", "sel.last")
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
        except:
            pass

    def paste(self):
        try:
            self.code.insert("insert", self.root.clipboard_get())
            self.update()
        except:
            pass

    # =========================================================
    # PARSER
    # =========================================================
    def parse(self, txt):
        if "NX" not in txt:
            return None, "Bad Syntax: Missing NX"
        if "FORMAT:" not in txt:
            return None, "Bad Syntax: Missing FORMAT"
        if "SIZE:" not in txt:
            return None, "Bad Syntax: Missing SIZE"
        if "DATA:" not in txt:
            return None, "Bad Syntax: Missing DATA"

        try:
            header, rest = txt.split("DATA:", 1)

            fmt = header.split("FORMAT:")[1].split(";")[0]
            size = header.split("SIZE:")[1].split(";")[0]
            w, h = map(int, size.strip("[]").split(","))

            # ================= INFO =================
            info = {}
            if "INFO:" in rest:
                data_part, info_part = rest.split("INFO:", 1)

                if "(" in info_part:
                    block = info_part.split("(",1)[1].split(")",1)[0]
                    for item in block.split(";"):
                        if ":" in item:
                            k,v = item.split(":",1)
                            info[k.strip()] = v.strip('"')
            else:
                data_part = rest

            # ================= PIXELS =================
            pixels = []
            for line in data_part.strip().split("\n"):
                for p in line.split(";"):
                    if p.strip():
                        r,g,b = p.split(",")
                        pixels.append((int(r,16), int(g,16), int(b,16)))

            if len(pixels) != w * h:
                return None, f"Size mismatch: expected {w*h}, got {len(pixels)}"

            return (fmt, w, h, pixels, info), None

        except Exception as e:
            return None, f"Bad Syntax: {str(e)}"

    # =========================================================
    # LIVE UPDATE
    # =========================================================
    def update(self):
        txt = self.code.get("1.0", "end")

        result, error = self.parse(txt)

        if error:
            self.err.config(text=error, fg="red")
            self.canvas.delete("all")
            self.info_label.config(text="ERROR")
            return

        fmt, w, h, pixels, info = result

        self.err.config(text="OK", fg="green")

        self.render(w, h, pixels)
        self.show_info(info)

    # =========================================================
    # INFO
    # =========================================================
    def show_info(self, info):
        if not info:
            self.info_label.config(text="No INFO")
            return

        self.info_label.config(text="\n".join(f"{k}: {v}" for k,v in info.items()))

    # =========================================================
    # RENDER
    # =========================================================
    def render(self, w, h, pixels):
        self.canvas.delete("all")

        size = max(2, min(40, 420 // max(w, h)))

        i = 0
        for y in range(h):
            for x in range(w):
                if i >= len(pixels):
                    return

                r,g,b = pixels[i]
                col = f"#{r:02x}{g:02x}{b:02x}"

                self.canvas.create_rectangle(
                    x*size, y*size,
                    (x+1)*size, (y+1)*size,
                    fill=col,
                    outline=""
                )
                i += 1


# ================= RUN =================
root = tk.Tk()
app = NXLiveIDE(root)
root.mainloop()