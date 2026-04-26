NX README (Human-Readable Image Format)

------------------------------------------------------------
WHAT IS NX?
------------------------------------------------------------

NX is a simple, text-based image format designed to store pixel art and images in a way that humans can read and edit directly.

Instead of being compressed or binary, NX files are written like plain text, making them easy to debug, modify, and experiment with.

------------------------------------------------------------
WHY NX EXISTS
------------------------------------------------------------

NX was created for:
- Learning how image formats work
- Easy pixel editing in text files
- Experimental graphics systems
- Custom engines and tools
- Education and prototyping

It is NOT meant to replace optimized image formats.

------------------------------------------------------------
SUPPORTED FORMATS
------------------------------------------------------------

NX currently supports 3 formats:

1) RGB_HEX
2) RGBA_HEX
3) INDEXED

------------------------------------------------------------
1. RGB_HEX FORMAT
------------------------------------------------------------

Structure:
FORMAT:RGB_HEX;SIZE:[width,height];

DATA:
FF,00,00;00,FF,00;00,00,FF;

Description:
- Each pixel has R,G,B values in hex (00–FF)
- No transparency
- Fully opaque pixels only

Best for:
- Pixel art
- Simple images

------------------------------------------------------------
2. RGBA_HEX FORMAT
------------------------------------------------------------

Structure:
FORMAT:RGBA_HEX;SIZE:[width,height];

DATA:
FF,00,00,FF;00,FF,00,80;00,00,FF,00;

Description:
- Each pixel has R,G,B,A values
- Alpha controls transparency:
  - 255 = fully opaque
  - 0   = fully transparent

Best for:
- UI graphics
- Transparent sprites
- Visual effects

------------------------------------------------------------
3. INDEXED FORMAT
------------------------------------------------------------

Structure:
FORMAT:INDEXED;SIZE:[width,height];

PALETTE:
0:255,0,0;
1:0,255,0;
2:0,0,255;

DATA:
0;1;2;0;1;

Description:
- Pixels store an index instead of color
- Colors are defined in a PALETTE
- Index IDs can be ANYTHING (0, -1, 2763, "red", etc.)

Best for:
- Efficient color reuse
- Palette-based images
- Experimental systems

------------------------------------------------------------
DATA RULES
------------------------------------------------------------

- Pixels are stored left -> right, top -> bottom
- Each pixel is separated by ";"
- Each row is separated by a newline
- Values are hex (RGB/RGBA) or index (INDEXED)

------------------------------------------------------------
INFO SECTION (OPTIONAL)
------------------------------------------------------------

INFO:
(TITLE:"Example";
AUTHOR:"User";
VERSION:"1.0";
COMMENT:"Any text here";)

- Stores metadata
- Fully optional
- Unlimited key-value fields

------------------------------------------------------------
FEATURES OF NX ECOSYSTEM
------------------------------------------------------------

- Pixel editor with tools (pencil, fill, erase, picker)
- Transparency support (RGBA)
- Indexed color system with custom IDs
- Palette editing system
- PNG ↔ NX conversion
- Live preview editors
- Debugging and syntax checking tools

------------------------------------------------------------
DESIGN PHILOSOPHY
------------------------------------------------------------

NX is designed to be:

- Human-readable
- Easy to modify manually
- Flexible and experimental
- Educational
- Cross-language friendly

------------------------------------------------------------
LIMITATIONS
------------------------------------------------------------

- No compression
- Large file sizes
- Not optimized for distribution
- Requires custom parsers
- Less efficient than standard image formats

------------------------------------------------------------
SUMMARY
------------------------------------------------------------

NX is not just a format.

It is a way to *see images as text*,
and understand how pixels are built from the ground up.
