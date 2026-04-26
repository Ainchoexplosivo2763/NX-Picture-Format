import tkinter as tk
from tkinter import filedialog, colorchooser, simpledialog, messagebox
from PIL import Image

class NXEditorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("NX Editor PRO 😈")

        # estado
        self.w, self.h = 16, 16
        self.pixels = [(255,255,255)] * (self.w*self.h)
        self.color = (255,0,0)
        self.show_grid = True
        self.tool = "pencil"

        self.update_pix()

        # canvas
        self.canvas = tk.Canvas(root, width=self.w*self.pix, height=self.h*self.pix)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_click)

        # toolbar
        bar = tk.Frame(root); bar.pack()

        tk.Button(bar, text="Color", command=self.pick_color).pack(side="left")
        tk.Button(bar, text="Pencil", command=lambda: self.set_tool("pencil")).pack(side="left")
        tk.Button(bar, text="Fill", command=lambda: self.set_tool("fill")).pack(side="left")
        tk.Button(bar, text="Eraser", command=lambda: self.set_tool("eraser")).pack(side="left")
        tk.Button(bar, text="Picker", command=lambda: self.set_tool("picker")).pack(side="left")

        tk.Button(bar, text="Grid", command=self.toggle_grid).pack(side="left")
        tk.Button(bar, text="Resize", command=self.resize_canvas).pack(side="left")

        tk.Button(bar, text="Guardar NX", command=self.save_nx).pack(side="left")
        tk.Button(bar, text="Cargar NX", command=self.load_nx).pack(side="left")

        tk.Button(bar, text="PNG→NX", command=self.import_png).pack(side="left")
        tk.Button(bar, text="NX→PNG", command=self.export_png).pack(side="left")

        # INFO panel
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

    # =========================
    def update_pix(self):
        self.pix = max(2, min(40, 600 // max(self.w, self.h)))

    def set_tool(self, t):
        self.tool = t

    def toggle_grid(self):
        self.show_grid = not self.show_grid
        self.draw()

    def pick_color(self):
        c = colorchooser.askcolor()[0]
        if c:
            self.color = tuple(int(v) for v in c)

    def resize_canvas(self):
        w = simpledialog.askinteger("Ancho", "Nuevo ancho:", initialvalue=self.w)
        h = simpledialog.askinteger("Alto", "Nuevo alto:", initialvalue=self.h)
        if not w or not h:
            return

        new_pixels = [(255,255,255)] * (w*h)
        for y in range(min(self.h, h)):
            for x in range(min(self.w, w)):
                new_pixels[y*w + x] = self.pixels[y*self.w + x]

        self.w, self.h = w, h
        self.pixels = new_pixels

        self.update_pix()
        self.canvas.config(width=self.w*self.pix, height=self.h*self.pix)
        self.draw()

    # =========================
    def draw(self):
        self.canvas.delete("all")
        for y in range(self.h):
            for x in range(self.w):
                i = y*self.w + x
                r,g,b = self.pixels[i]
                color = f"#{r:02x}{g:02x}{b:02x}"

                self.canvas.create_rectangle(
                    x*self.pix, y*self.pix,
                    (x+1)*self.pix, (y+1)*self.pix,
                    fill=color,
                    outline="black" if self.show_grid else ""
                )

    def on_click(self, event):
        x = event.x // self.pix
        y = event.y // self.pix
        if not (0 <= x < self.w and 0 <= y < self.h):
            return

        i = y*self.w + x

        if self.tool == "pencil":
            self.pixels[i] = self.color
        elif self.tool == "eraser":
            self.pixels[i] = (255,255,255)
        elif self.tool == "picker":
            self.color = self.pixels[i]
        elif self.tool == "fill":
            self.flood_fill(x, y, self.pixels[i], self.color)

        self.draw()

    def flood_fill(self, x, y, target, replacement):
        if target == replacement:
            return

        stack = [(x,y)]
        while stack:
            cx, cy = stack.pop()
            i = cy*self.w + cx
            if self.pixels[i] != target:
                continue

            self.pixels[i] = replacement

            for nx, ny in [(cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)]:
                if 0 <= nx < self.w and 0 <= ny < self.h:
                    stack.append((nx,ny))

    # =========================
    def add_info_field(self, key="", value=""):
        frame = tk.Frame(self.info_container)
        frame.pack()

        k = tk.Entry(frame, width=12)
        k.insert(0, key)
        k.pack(side="left")

        tk.Label(frame, text=":").pack(side="left")

        v = tk.Entry(frame, width=20)
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

    # =========================
    def save_nx(self):
        path = filedialog.asksaveasfilename(defaultextension=".nx")
        if not path:
            return

        info = self.collect_info()

        with open(path,"w") as f:
            f.write("NX\n")
            f.write(f"FORMAT:RGB_HEX;SIZE:[{self.w},{self.h}];\n")
            f.write("DATA:\n")

            i = 0
            for y in range(self.h):
                for x in range(self.w):
                    r,g,b = self.pixels[i]
                    f.write(f"{r:02X},{g:02X},{b:02X};")
                    i+=1
                f.write("\n")

            if info:
                f.write("\nINFO:(")
                for k,v in info.items():
                    f.write(f'{k}:"{v}";')
                f.write(")\n")

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

        pix=[]
        for line in data_part.strip().split("\n"):
            for p in line.split(";"):
                if p:
                    r,g,b = p.split(",")
                    pix.append((int(r,16),int(g,16),int(b,16)))

        info={}
        if info_part:
            for campo in info_part.strip().strip("()").split(";"):
                if campo:
                    k,v = campo.split(":",1)
                    info[k]=v.strip('"')

        self.w,self.h = w,h
        self.pixels = pix

        self.update_pix()
        self.canvas.config(width=self.w*self.pix, height=self.h*self.pix)

        self.load_info_into_ui(info)
        self.draw()

    # =========================
    def import_png(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        img = Image.open(path).convert("RGB")
        self.w,self.h = img.size
        self.pixels = list(img.getdata())

        self.update_pix()
        self.canvas.config(width=self.w*self.pix, height=self.h*self.pix)
        self.draw()

    def export_png(self):
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if not path:
            return

        img = Image.new("RGB",(self.w,self.h))
        img.putdata(self.pixels)
        img.save(path)


# =========================

root = tk.Tk()
app = NXEditorPro(root)
root.mainloop()