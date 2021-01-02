#!/usr/bin/python3
import datetime
import math
import cairo

light_tone_lut = [1.0, 0.66, 0.33, 0.0]
dark_tone_lut = [0.0, 0.33, 0.66, 1.0]
tone_lut = light_tone_lut
draw_seconds=True

def set_tone(context, value):
    shade = tone_lut[value-1]
    context.set_source_rgba(shade, shade, shade, 1.0)

def init(invert=False, noseconds=False):
    global tone_lut
    tone_lut = dark_tone_lut if invert else light_tone_lut
    global draw_seconds
    draw_seconds = not noseconds



def draw_bg(context, width, height):
    context.save()
    context.rectangle(0, 0, width, height)
    set_tone(context, 1)
    context.fill()
    context.restore()

def draw_clockface(context, width, height, time):

    size = min(width, height)
    size *= 0.9
    scaling = size/175

    def xy(rotation):
        pos = rotation * 2*math.pi
        x = math.sin(pos)
        y = math.cos(pos)
        return (x, -y)

    #context should be a cairo drawing context
    #size should be the size of the clock
    #length should be a % (0 to 1) of how far the hand should extend
    #width should be a % (0 to 1) of how wide the hand should be
    #rotation should be a % value (0 to 1) with 0 being 12 o'clock
    def draw_hand(length, width, rotation, tone=4):
        context.save()        
        center = size/2
        context.move_to(center, center)
        context.set_line_width(width*4*scaling)
        x, y = xy(rotation)
        x *= center * length
        y *= center * length
        context.line_to(center+x, center+y)
        set_tone(context, tone)
        context.stroke()
        context.restore()

    def draw_hour_hand(time):
        fraction = (time.second + time.minute*60) / 3600.0
        rot = ((time.hour%12) + fraction) / 12.0
        draw_hand(0.4, 1.0, rot)

    def draw_minute_hand(time):
        fraction = time.second / 60.0
        rot = (time.minute + fraction) / 60.0
        draw_hand(0.7, 0.5, rot, 3)

    def draw_second_hand(time):
        rot = time.second / 60.0
        draw_hand(0.8, 0.2, rot, 2)

    def draw_center():
        center = size / 2
        context.move_to(center, center)

        radius = 5 * scaling
        set_tone(context, 4)
        context.arc(center, center, radius, 0, math.pi*2)
        context.fill()

        radius = 3 * scaling
        set_tone(context, 1)
        context.arc(center, center, radius, 0, math.pi*2)
        context.fill()

    def draw_hands(time):
        draw_hour_hand(time)
        draw_minute_hand(time)
        if draw_seconds: draw_second_hand(time)
        draw_center()


    def draw_face():
        context.save()
        set_tone(context, 2)
        c = size / 2
        context.set_line_width(2 * scaling)
        for i in range(1, 13):
            x, y = xy(i/12.0)
            x *= c
            y *= c
            context.move_to(c+x*0.92, c+y*0.92)
            context.line_to(c+x, c+y)
            context.stroke()
        set_tone(context, 4)
        context.set_line_width(2 * scaling)
        context.arc(c, c, c, 0, math.pi*2)
        context.stroke()
        context.restore()


    context.save()

    #translate for non-square surfaces
    if height > size:
        context.translate(0, (height-size)/2)
    if width > size:
        context.translate((width-size)/2, 0)

    #draw the clock face, the numbers and tick marks
    draw_face()

    #draw clock hands
    draw_hands(time)

    context.restore()

def draw_datestamp(context, screenwidth, screenheight, time):
    context.save()

    clocksize = min(screenwidth, screenheight)
    height = (screenheight - clocksize) / 2.0
    width = screenwidth
    context.set_font_size(height * 0.3)
    text = time.strftime("%A, %-d %B %Y")
    extents = context.text_extents(text)
    context.move_to((width - extents.width) / 2.0, screenheight - (height - extents.height) / 2.0)
    context.show_text(text)

    context.restore()

def draw_timestamp(context, screenwidth, screenheight, time):
    context.save()

    clocksize = min(screenwidth, screenheight)
    height = (screenheight - clocksize) / 2.0
    width = screenwidth
    context.set_font_size(height * 0.7)
    text = time.strftime("%H:%M")
    extents = context.text_extents(text)
    context.move_to((width - extents.width) / 2.0, height - (height - extents.height) / 2.0)
    context.show_text(text)

    context.restore()
    
#accepts (and returns) a cairo surface with the given width and height, containing the image to be displayed
def draw(surface):
    width = surface.get_width()
    height = surface.get_height()
    time = datetime.datetime.now()
    context = cairo.Context(surface)
    context.set_line_cap(cairo.LineCap.ROUND)
    context.select_font_face("Futura Lt BT", cairo.FontSlant.NORMAL)
    set_tone(context, 4)

    draw_bg(context, width, height)
    draw_clockface(context, width, height, time)
    draw_timestamp(context, width, height, time)
    draw_datestamp(context, width, height, time)

    surface.flush()
