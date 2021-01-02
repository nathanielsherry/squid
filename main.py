#!/usr/bin/python3
import plac, importlib, datetime, pause, cairo, sys, os
import clock

currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentdir + "/squid")

#from drivers.waveshare.epd27bw import display
from squid.drivers.filesystem import display


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

    #import various widgets
    from squid.widgets import FloodFill
    from squid.widgets.layout import Stack, HBox
    from squid.widgets.clock import AnalogClock, DigitalClock, Date

    #create and compose widgets
    stack = Stack()
    stack.add_child(FloodFill(1))
    hbox = HBox()
    stack.add_child(hbox)
    hbox.add_child(DigitalClock())
    hbox.add_child(AnalogClock())
    hbox.add_child(Date())

    def load_display_driver(name):
        return importlib.import_module("squid.drivers." + name + ".display")

    def draw():
        
        #create a new drawing context for this surface
        context = cairo.Context(surface)
        context.set_line_cap(cairo.LineCap.ROUND)
        context.select_font_face("Futura Lt BT", cairo.FontSlant.NORMAL)
        
        stack.draw(context, surface.get_width(), surface.get_height())
        display.show(surface)


    #initialize frame count
    count = 0
    
    #load & init display driver
    display = load_display_driver(driver)
    display.init(filename=filename)
    
    #init widget settings
    from squid.widgets import init as widget_init
    widget_init(invert=invert, noseconds=noseconds)
    
    #create the cairo surface
    surface = display.get_surface()
    
    #start time for the interval timer
    nexttime = datetime.datetime.now()
    while True:
        draw()
        count += 1
        if count == framecount: break
        nexttime = nexttime + datetime.timedelta(seconds=interval)
        pause.until(nexttime)


if __name__ == '__main__':
    plac.call(main)

