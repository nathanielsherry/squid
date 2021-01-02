#!/usr/bin/python3
import plac, importlib, datetime, pause
import clock
#from drivers.waveshare.epd27bw import display
from drivers.filesystem import display
#
# +------------+
# | INTERFACES |
# +------------+
# 
# Display
#  init(): called once at startup
#  show(cairo_surface): called to update the display
#  get_width(), get_height(): return dimenstions of display
# 
# Clock
#  init(invert): sets persistent options on the clock
#  draw(width, height): returns a cairo surface of the given dimensions to be drawn
# 
#  


def main(
        interval: ('Frame interval in seconds', 'option', 'i')=1,
        framecount: ('Frames to generate, -1 is no limit', 'option', 'f')=-1,
        driver: ('Driver backend to use, default is filesystem', 'option', 'd')='filesystem',
        invert: ('Invert light and dark tones', 'flag', 'v')=False,
        noseconds: ('Don\'t show the second hand', 'flag', 'n')=False,
        filename: ('Output filename (if any) where "%" is epoch timestamp', 'option', 'p')="clock.png",
    ):

    def load_display_driver(name):
        return importlib.import_module("drivers." + name + ".display")

    def draw():
        clock.draw(surface)
        display.show(surface)

    count = 0
    display = load_display_driver(driver)
    display.init(filename=filename)
    clock.init(invert=invert, noseconds=noseconds)
    surface = display.get_surface()

    nexttime = datetime.datetime.now()
    while True:
        draw()
        count += 1
        if count == framecount: break
        nexttime = nexttime + datetime.timedelta(seconds=interval)
        pause.until(nexttime)


if __name__ == '__main__':
    plac.call(main)

