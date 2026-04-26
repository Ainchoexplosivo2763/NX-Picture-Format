import tkinter as tk
from tkinter import filedialog, colorchooser, simpledialog, messagebox
from PIL import Image

class NXEditorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("NX Editor PRO 😈 (RGBA + INFO)")

        # estado
        self.w, self.h = 16, 16
        self.pixels = [(255,255,255,255)] * (self.w*self.h)

        self.color = (255,0,0,255)
        self.show_grid = True
        self.tool = "pencil"

        self.alpha_global = 255  # 🔥 nuevo control

        self.update_pix()

        # ================= CANVAS =================
        self.canvas = tk.Canvas(root, width=self.w*self.pix, height=self.h*self.pix)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_click)

        # ================= TOOLBAR =================
        bar = tk.Frame(root)
        bar.pack()

        tk.Button(bar, text="Color", command=self.pick_color).pack(side="left")
        tk.Button(bar, text="Pencil", command=lambda: self.set_tool("pencil")).pack(side="left")
        tk.Button(bar, text="Eraser (Transparent)", command=self.use_eraser).pack(side="left")

        tk.Button(bar, text="Alpha", command=self.set_alpha).pack(side="left")  # 🔥 NUEVO

        tk.Button(bar, text="Grid", command=self.toggle_grid).pack(side="left")
        tk.Button(bar, text="Resize", command=self.resize_canvas).pack(side="left")

        tk.Button(bar, text="Guardar NX", command=self.save_nx).pack(side="left")
        tk.Button(bar, text="Cargar NX", command=self.load_nx).pack(side="left")

        tk.Button(bar, text="PNG→NX", command=self.import_png).pack(side="left")
        tk.Button(bar, text="NX→PNG", command=self.export_png).pack(side="left")

        # ================= INFO PANEL =================
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(fill="x")

        tk.Label(self.info_frame, text="INFO").pack()

        self.info_container = tk.Frame(self.info_frame)
        self.info_container.pack()

        self.info_fields = []

        btns = tk.Frame(self.info_frame)
        btns.pack()

        tk.Button(btns, text="+", command=self.add_info_field).pack(side="left")
        tk.Button(btns, text="-", command=self.remove_info_field).pack(side="left")

        self.add_info_field("VERSION", "1.0")
        self.add_info_field("AUTHOR", "NemKazi")

        self.draw()

    # ================= PIX SIZE =================
    def update_pix(self):
        self.pix = max(2, min(40, 600 // max(self.w, self.h)))

    # ================= TOOLS =================
    def set_tool(self, t):
        self.tool = t

    def use_eraser(self):
        self.tool = "eraser"

    def toggle_grid(self):
        self.show_grid = not self.show_grid
        self.draw()

    def pick_color(self):
        c = colorchooser.askcolor()[0]
        if c:
            self.color = (int(c[0]), int(c[1]), int(c[2]), self.alpha_global)

    # ================= 🔥 ALPHA CONTROL =================
    def set_alpha(self):
        a = simpledialog.askinteger("Alpha", "0 = invisible, 255 = solid", initialvalue=self.alpha_global, minvalue=0, maxvalue=255)
        if a is not None:
            self.alpha_global = a
            r,g,b,_ = self.color
            self.color = (r,g,b,a)

    # ================= DRAW =================
    def draw(self):
        self.canvas.delete("all")

        for y in range(self.h):
            for x in range(self.w):
                i = y*self.w + x
                r,g,b,a = self.pixels[i]

                if a == 0:
                    color = "#cccccc"
                else:
                    color = f"#{r:02x}{g:02x}{b:02x}"

                self.canvas.create_rectangle(
                    x*self.pix, y*self.pix,
                    (x+1)*self.pix, (y+1)*self.pix,
                    fill=color,
                    outline="black" if self.show_grid else ""
                )

    # ================= CLICK =================
    def on_click(self, event):
        x = event.x // self.pix
        y = event.y // self.pix

        if not (0 <= x < self.w and 0 <= y < self.h):
            return

        i = y*self.w + x

        if self.tool == "pencil":
            self.pixels[i] = self.color

        elif self.tool == "eraser":
            self.pixels[i] = (0,0,0,0)

        self.draw()

    # ================= RESIZE =================
    def resize_canvas(self):
        w = simpledialog.askinteger("W", "Width:", initialvalue=self.w)
        h = simpledialog.askinteger("H", "Height:", initialvalue=self.h)
        if not w or not h:
            return

        new_pixels = [(0,0,0,0)] * (w*h)

        for y in range(min(self.h,h)):
            for x in range(min(self.w,w)):
                new_pixels[y*w + x] = self.pixels[y*self.w + x]

        self.w,self.h = w,h
        self.pixels = new_pixels

        self.update_pix()
        self.canvas.config(width=w*self.pix, height=h*self.pix)
        self.draw()

    # ================= INFO =================
    def add_info_field(self, key="", value=""):
        frame = tk.Frame(self.info_container)
        frame.pack()

        k = tk.Entry(frame, width=12)
        k.insert(0, key)
        k.pack(side="left")

        tk.Label(frame, text=":").pack(side="left")

        v = tk.Entry(frame, width=25)
        v.insert(0, value)
        v.pack(side="left")

        self.info_fields.append((frame,k,v))

    def remove_info_field(self):
        if self.info_fields:
            frame,_,_ = self.info_fields.pop()
            frame.destroy()

    def collect_info(self):
        info = {}
        for _,k,v in self.info_fields:
            key = k.get().strip()
            val = v.get().strip()
            if key:
                info[key] = val
        return info

    def load_info_into_ui(self, info):
        for frame,_,_ in self.info_fields:
            frame.destroy()
        self.info_fields.clear()

        for k,v in info.items():
            self.add_info_field(k,v)

    # ================= SAVE =================
    def save_nx(self):
        path = filedialog.asksaveasfilename(defaultextension=".nx")
        if not path:
            return

        info = self.collect_info()

        with open(path,"w") as f:
            f.write("NX\n")
            f.write(f"FORMAT:RGBA_HEX;SIZE:[{self.w},{self.h}];\n")
            f.write("DATA:\n")

            i=0
            for y in range(self.h):
                for x in range(self.w):
                    r,g,b,a = self.pixels[i]
                    f.write(f"{r:02X},{g:02X},{b:02X},{a:02X};")
                    i+=1
                f.write("\n")

            if info:
                f.write("\nINFO:(")
                for k,v in info.items():
                    f.write(f'{k}:"{v}";')
                f.write(")\n")

    # ================= LOAD =================
    def load_nx(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        txt = open(path).read()

        header, rest = txt.split("DATA:",1)

        size = header.split("SIZE:")[1].split(";")[0]
        w,h = map(int,size.strip("[]").split(","))

        if "INFO:" in rest:
            data_part, info_part = rest.split("INFO:",1)
        else:
            data_part = rest
            info_part = ""

        pix = []
        for line in data_part.strip().split("\n"):
            for p in line.split(";"):
                if p:
                    vals = p.split(",")
                    r,g,b,a = vals if len(vals)==4 else (*vals,"FF")

                    pix.append((
                        int(r,16),
                        int(g,16),
                        int(b,16),
                        int(a,16)
                    ))

        info = {}
        if info_part:
            for c in info_part.strip().strip("()").split(";"):
                if c:
                    k,v = c.split(":",1)
                    info[k]=v.strip('"')

        self.w,self.h = w,h
        self.pixels = pix

        self.update_pix()
        self.canvas.config(width=w*self.pix, height=h*self.pix)

        self.load_info_into_ui(info)
        self.draw()

    # ================= PNG =================
    def import_png(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        img = Image.open(path).convert("RGBA")

        self.w,self.h = img.size
        self.pixels = list(img.getdata())

        self.update_pix()
        self.canvas.config(width=self.w*self.pix, height=self.h*self.pix)
        self.draw()

    def export_png(self):
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if not path:
            return

        img = Image.new("RGBA",(self.w,self.h))
        img.putdata(self.pixels)
        img.save(path)


# =========================

root = tk.Tk()
app = NXEditorPro(root)
root.mainloop()