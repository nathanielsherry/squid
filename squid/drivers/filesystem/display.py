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
    fn = filename.replace('$epoch', str(int(time.time())))
    #surface.write_to_png(fn)
    pil_image = cairo_to_pil(surface)
    pil_image.save(fn)

def cairo_to_pil(cairo_surface):
    w = cairo_surface.get_width()
    h = cairo_surface.get_height()
    data = cairo_surface.get_data()
    from PIL import Image
    pil_image = Image.frombuffer("RGBA", (w, h), data, "raw", "RGBA", 0, 1)
    return pil_image

def get_surface(): return cairo.ImageSurface(cairo.Format.ARGB32, get_width(), get_height())
def get_width(): return int(width*0.8)
def get_height(): return int(height*0.8)
