import tkinter as tk
from tkinter import filedialog, simpledialog
import random

class NXRGBA_Generator:
    def __init__(self, root):
        self.root = root
        self.root.title("NX RGBA Generator 🌈")

        self.w, self.h = 64, 64
        self.pixels = []

        self.canvas = tk.Canvas(root, width=600, height=600, bg="black")
        self.canvas.pack()

        bar = tk.Frame(root)
        bar.pack()

        tk.Button(bar, text="Generate RGBA", command=self.generate).pack(side="left")
        tk.Button(bar, text="Save .nx", command=self.save).pack(side="left")
        tk.Button(bar, text="Random Noise", command=self.noise).pack(side="left")
        tk.Button(bar, text="Gradient RGBA", command=self.gradient).pack(side="left")

        self.generate()

    # =========================
    # PIX SIZE
    # =========================
    def pix(self):
        return max(2, 600 // self.w)

    # =========================
    # GENERATE FULL RGBA SAMPLE
    # =========================
    def generate(self):
        self.pixels = []

        for y in range(self.h):
            for x in range(self.w):
                r = int((x / self.w) * 255)
                g = int((y / self.h) * 255)
                b = random.randint(0, 255)
                a = random.randint(0, 255)  # 🔥 alpha real

                self.pixels.append((r, g, b, a))

        self.draw()

    # =========================
    # NOISE MODE
    # =========================
    def noise(self):
        self.pixels = [
            (random.randint(0,255),
             random.randint(0,255),
             random.randint(0,255),
             random.randint(0,255))
            for _ in range(self.w*self.h)
        ]
        self.draw()

    # =========================
    # GRADIENT RGBA
    # =========================
    def gradient(self):
        self.pixels = []

        for y in range(self.h):
            for x in range(self.w):
                r = int((x / self.w) * 255)
                g = int((y / self.h) * 255)
                b = 255 - r
                a = int(((x + y) / (self.w + self.h)) * 255)

                self.pixels.append((r,g,b,a))

        self.draw()

    # =========================
    # DRAW
    # =========================
    def draw(self):
        self.canvas.delete("all")
        p = self.pix()

        for i, (r,g,b,a) in enumerate(self.pixels):
            x = (i % self.w) * p
            y = (i // self.w) * p

            # alpha visual (simulado con mezcla gris)
            bg = int(a)
            color = f"#{r:02x}{g:02x}{b:02x}"

            self.canvas.create_rectangle(
                x, y, x+p, y+p,
                fill=color,
                outline=""
            )

    # =========================
    # SAVE NX RGBA
    # =========================
    def save(self):
        path = filedialog.asksaveasfilename(defaultextension=".nx")
        if not path:
            return

        with open(path, "w") as f:
            f.write("NX\n")
            f.write(f"FORMAT:RGBA_HEX;SIZE:[{self.w},{self.h}];\n")
            f.write("DATA:\n")

            i = 0
            for y in range(self.h):
                for x in range(self.w):
                    r,g,b,a = self.pixels[i]
                    f.write(f"{r:02X},{g:02X},{b:02X},{a:02X};")
                    i += 1
                f.write("\n")

            f.write("\nINFO:(TITLE:\"RGBA Generator\";)\n")


# =========================
root = tk.Tk()
app = NXRGBA_Generator(root)
root.mainloop()