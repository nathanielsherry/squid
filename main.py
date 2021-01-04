#!/usr/bin/python3
import plac, importlib, datetime, pause, cairo, sys, os, math

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
# Widgets
#  init(invert, noseconds): sets persistent options on the clock
#  draw(context, width, height): returns a cairo surface of the given dimensions to be drawn
# 
#  


def main(
        interval: ('Frame interval in seconds', 'option', 'i')=1,
        framecount: ('Frames to generate, -1 is no limit', 'option', 'f')=-1,
        driver: ('Driver backend to use, default is filesystem', 'option', 'd')='filesystem',
        invert: ('Invert light and dark tones', 'flag', 'v')=False,
        noseconds: ('Don\'t show the second hand', 'flag', 'n')=False,
        filename: ('Output filename (if any) where $epoch is epoch timestamp', 'option', 'p')="clock.png",
        rotate: ('Rotate the image 180 degrees', 'flag', 'r')=False,
    ):

    #import various widgets
    from squid.widgets.decor import FloodFill, Notches, Border, NotchedBorder
    from squid.widgets.layout import Stack, HBox
    from squid.widgets.clock import AnalogClock, DigitalClock, Date

    #create and compose widgets
    border_width = 1
    notch_width = 10
    background = Stack.build(FloodFill(2))
    digital_clock = DigitalClock(width_percent=55)
    analog_clock = Border(5, 0, AnalogClock(draw_seconds=not noseconds))
    hbox = HBox.build(digital_clock, analog_clock, Date())
    
    stack = Stack.build(
        background, 
        Border(border_width*2, 0,
        NotchedBorder(
            border_width, 
            4, 
            notch_width,
            Border(border_width, 0, hbox),
            inner_tone = 1         
    )))


    def load_display_driver(name):
        return importlib.import_module("squid.drivers." + name + ".display")

    def draw():
        
        #create a new drawing context for this surface
        context = cairo.Context(surface)
        if rotate:
            width = surface.get_width()
            height = surface.get_height()
            context.translate(width/2, height/2)
            context.rotate(math.pi)
            context.translate(-width/2, -height/2)
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
    from squid.palettes import init as palette_init
    palette_init(invert=invert)
    
    #create the cairo surface
    surface = display.get_surface()
    
    #start time for the interval timer
    nexttime = datetime.datetime.now()
    #If the interval is a whole number of minutes, align the next interval
    #to the minute mark
    if interval % 60 == 0:
        nexttime = datetime.datetime(
            year = nexttime.year,
            month = nexttime.month,
            day = nexttime.day,
            hour = nexttime.hour,
            minute = nexttime.minute,
        )
    while True:
        draw()
        count += 1
        if count == framecount: break
        delta = datetime.timedelta(seconds=interval)
        nexttime = nexttime + delta
        pause.until(nexttime)


if __name__ == '__main__':
    plac.call(main)

