import tkinter as tk
from tkinter import filedialog, colorchooser, simpledialog, messagebox
from PIL import Image

class NXEditorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("NX INDEX Editor PRO 😈")

        # ================= GRID =================
        self.w, self.h = 16, 16
        self.update_pix()

        # pixels = INDEXES
        self.pixels = [0] * (self.w * self.h)

        # palette index -> (r,g,b)
        self.palette = {
            "0": (255, 255, 255)
        }

        self.current_index = "0"
        self.show_grid = True
        self.tool = "pencil"

        # ================= CANVAS =================
        self.canvas = tk.Canvas(root, width=self.w*self.pix, height=self.h*self.pix)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_click)

        # ================= TOOLBAR =================
        bar = tk.Frame(root)
        bar.pack()

        tk.Button(bar, text="Set Index", command=self.set_index).pack(side="left")
        tk.Button(bar, text="+INDEX", command=self.add_index).pack(side="left")
        tk.Button(bar, text="Change Color", command=self.change_index_color).pack(side="left")

        tk.Button(bar, text="Pencil", command=lambda: self.set_tool("pencil")).pack(side="left")
        tk.Button(bar, text="Picker", command=lambda: self.set_tool("picker")).pack(side="left")
        tk.Button(bar, text="Fill", command=lambda: self.set_tool("fill")).pack(side="left")
        tk.Button(bar, text="Eraser", command=lambda: self.set_tool("eraser")).pack(side="left")

        tk.Button(bar, text="Grid", command=self.toggle_grid).pack(side="left")
        tk.Button(bar, text="Resize", command=self.resize_canvas).pack(side="left")

        tk.Button(bar, text="Save NX", command=self.save_nxi).pack(side="left")
        tk.Button(bar, text="Load NX", command=self.load_nxi).pack(side="left")

        tk.Button(bar, text="PNG→NX", command=self.import_png).pack(side="left")
        tk.Button(bar, text="NX→PNG", command=self.export_png).pack(side="left")

        # ================= INFO =================
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

    # ================= TOOL =================
    def set_tool(self, t):
        self.tool = t

    def toggle_grid(self):
        self.show_grid = not self.show_grid
        self.draw()

    # ================= INDEX =================
    def add_index(self):
        idx = simpledialog.askstring("INDEX ID", "ID (0, -1, hello...):")
        if idx is None:
            return

        color = colorchooser.askcolor()[0]
        if color:
            self.palette[idx] = tuple(map(int, color))
            self.current_index = idx
            self.draw()

    def set_index(self):
        idx = simpledialog.askstring("Select Index", "Index:")
        if idx in self.palette:
            self.current_index = idx
        else:
            messagebox.showerror("Error", "Index no existe")

    def change_index_color(self):
        idx = simpledialog.askstring("Change Index", "Index:")
        if idx not in self.palette:
            messagebox.showerror("Error", "No existe")
            return

        color = colorchooser.askcolor()[0]
        if color:
            self.palette[idx] = tuple(map(int, color))
            self.draw()

    # ================= DRAW =================
    def draw(self):
        self.canvas.delete("all")

        for y in range(self.h):
            for x in range(self.w):
                i = y*self.w + x
                idx = str(self.pixels[i])

                if idx in self.palette:
                    r,g,b = self.palette[idx]
                else:
                    r,g,b = (255,0,255)  # error color

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
            self.pixels[i] = self.current_index

        elif self.tool == "eraser":
            self.pixels[i] = "0"

        elif self.tool == "picker":
            self.current_index = self.pixels[i]

        elif self.tool == "fill":
            self.flood_fill(x, y, self.pixels[i], self.current_index)

        self.draw()

    # ================= FLOOD FILL =================
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

            for nx, ny in [(1,0),(-1,0),(0,1),(0,-1)]:
                xx, yy = cx+nx, cy+ny
                if 0 <= xx < self.w and 0 <= yy < self.h:
                    stack.append((xx,yy))

    # ================= RESIZE =================
    def resize_canvas(self):
        w = simpledialog.askinteger("W", "Width:", initialvalue=self.w)
        h = simpledialog.askinteger("H", "Height:", initialvalue=self.h)
        if not w or not h:
            return

        new_pixels = ["0"] * (w*h)

        for y in range(min(self.h,h)):
            for x in range(min(self.w,w)):
                new_pixels[y*w+x] = self.pixels[y*self.w+x]

        self.w,self.h = w,h
        self.pixels = new_pixels

        self.update_pix()
        self.canvas.config(width=w*self.pix,height=h*self.pix)
        self.draw()

    # ================= INFO =================
    def add_info_field(self, key="", value=""):
        f = tk.Frame(self.info_container)
        f.pack()

        k = tk.Entry(f,width=12)
        k.insert(0,key)
        k.pack(side="left")

        tk.Label(f,text=":").pack(side="left")

        v = tk.Entry(f,width=20)
        v.insert(0,value)
        v.pack(side="left")

        self.info_fields.append((f,k,v))

    def remove_info_field(self):
        if self.info_fields:
            f,_,_ = self.info_fields.pop()
            f.destroy()

    def collect_info(self):
        info={}
        for _,k,v in self.info_fields:
            key=k.get().strip()
            val=v.get().strip()
            if key:
                info[key]=val
        return info

    def load_info_into_ui(self, info):
        for f,_,_ in self.info_fields:
            f.destroy()
        self.info_fields.clear()

        for k,v in info.items():
            self.add_info_field(k,v)

    # ================= SAVE =================
    def save_nxi(self):
        path = filedialog.asksaveasfilename(defaultextension=".nx")
        if not path:
            return

        info = self.collect_info()

        with open(path,"w",encoding="utf-8") as f:
            f.write("NX\n")
            f.write(f"FORMAT:INDEXED;SIZE:[{self.w},{self.h}];\n")

            # palette
            f.write("PALETTE:\n")
            for k,(r,g,b) in self.palette.items():
                f.write(f"{k}:{r},{g},{b};\n")

            # data
            f.write("DATA:\n")
            i=0
            for y in range(self.h):
                for x in range(self.w):
                    f.write(f"{self.pixels[i]};")
                    i+=1
                f.write("\n")

            if info:
                f.write("\nINFO:(")
                for k,v in info.items():
                    f.write(f'{k}:"{v}";')
                f.write(")\n")

    # ================= LOAD (FIXED) =================
    def load_nxi(self):
        path = filedialog.askopenfilename(filetypes=[("NX","*.nx"), ("NX","*.NX")])
        if not path:
            return

        txt=open(path,"r",encoding="utf-8").read()

        try:
            header,rest = txt.split("DATA:",1)

            size = header.split("SIZE:")[1].split(";")[0]
            w,h = map(int,size.strip("[]").split(","))

            # palette
            palette={}
            if "PALETTE:" in txt:
                pblock = txt.split("PALETTE:")[1].split("DATA:")[0]
                for line in pblock.splitlines():
                    if ":" in line:
                        k,v=line.split(":",1)
                        r,g,b=v.strip().strip(";").split(",")
                        palette[k]=(int(r),int(g),int(b))

            data_part = rest.split("INFO:")[0] if "INFO:" in rest else rest

            pixels=[]
            for p in data_part.replace("\n",";").split(";"):
                p=p.strip()
                if p=="":
                    continue
                try:
                    pixels.append(p)
                except:
                    pass

            self.w,self.h=w,h
            self.palette=palette
            self.pixels=pixels

            self.update_pix()
            self.canvas.config(width=w*self.pix,height=h*self.pix)
            self.draw()

        except Exception as e:
            messagebox.showerror("NXI Error",str(e))

    # ================= PNG =================
    def import_png(self):
        path=filedialog.askopenfilename()
        if not path:return

        img=Image.open(path).convert("RGB")
        self.w,self.h=img.size

        self.pixels=["0"]*(self.w*self.h)

        self.update_pix()
        self.canvas.config(width=self.w*self.pix,height=self.h*self.pix)
        self.draw()

    def export_png(self):
        path=filedialog.asksaveasfilename(defaultextension=".png")
        if not path:return

        img=Image.new("RGB",(self.w,self.h))
        data=[self.palette.get(p,(0,0,0)) for p in self.pixels]
        img.putdata(data)
        img.save(path)


# ================= RUN =================
root=tk.Tk()
app=NXEditorPro(root)
root.mainloop()