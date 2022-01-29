import cairo
from . import driver

epd = None
def init(**kwargs):
    global epd
    epd = driver.EPD()
    epd.init(mode=0)
    epd.Clear(0xFF)

def cairo_to_pil(cairo_surface):
    w = cairo_surface.get_width()
    h = cairo_surface.get_height()
    data = cairo_surface.get_data()
    from PIL import Image
    pil_image = Image.frombuffer("RGBA", (w, h), data, "raw", "RGBA", 0, 1)
    return pil_image
    
#accepts a cairo surface matching the width and height of this display and draws it
def show(surface):
    pil_image = cairo_to_pil(surface)
    epd.display_4Gray(epd.getbuffer_4Gray(pil_image))
    return

def get_surface(): return cairo.ImageSurface(cairo.Format.ARGB32, get_width(), get_height())
def get_width(): return epd.width
def get_height(): return epd.height
