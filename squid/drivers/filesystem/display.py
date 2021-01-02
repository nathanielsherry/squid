import cairo
import time

width = 176
height = 264
filename = "./clock.png"

def init(**kwargs):
    global width
    width = kwargs.get('width', width)
    global height
    height = kwargs.get('height', height)
    global filename
    filename = kwargs.get('filename', filename)

#accepts a cairo surface matching the width and height of this display and draws it
def show(surface):
    fn = filename.replace('%', str(int(time.time())))
    surface.write_to_png(fn)

def get_surface(): return cairo.ImageSurface(cairo.Format.ARGB32, get_width(), get_height())
def get_width(): return width
def get_height(): return height
