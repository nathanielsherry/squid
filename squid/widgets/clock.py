from squid.widgets.base import Component
from squid.widgets import set_tone
import math, datetime

class AnalogClock(Component):
    def __init__(self, draw_seconds=True):
        super().__init__()
        self._draw_seconds = draw_seconds
        
    def get_used_size(self, context, width, height):
        size = min(width, height)
        return (size, size)
        
    def draw(self, context, width, height):
        real_size = min(width, height)
        size = real_size * 0.9
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
            if self._draw_seconds: draw_second_hand(time)
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

        #translate for non-square surfaces
        if height > size:
            context.translate(0, (height-size)/2)
        if width > size:
            context.translate((width-size)/2, 0)

        #draw the clock face, the numbers and tick marks
        draw_face()

        #draw clock hands
        draw_hands(datetime.datetime.now())
        
        return (real_size, real_size)
        

class Text(Component):
    def __init__(self, width_percent=50):
        super().__init__()
        self._width_percent = width_percent
    
    def get_text(self): 
        raise Exception("Unimplemented")
    
    def calc_font_size(self, context, width, height):
        text = self.get_text()
        font_size = 1
        while True:
            context.set_font_size(font_size)
            extents = context.text_extents(self.get_text())
            if extents.width > width * self._width_percent/100.0: break
            if extents.height > height: break
            font_size += 1
        return font_size
    
    def get_used_size(self, context, width, height):
        context.set_font_size(self.calc_font_size(context, width, height))
        extents = context.text_extents(self.get_text())
        return (width, extents.height*1.2)

    def draw(self, context, width, height):
        set_tone(context, 4)
        text = self.get_text()
        context.set_font_size(self.calc_font_size(context, width, height))
        extents = context.text_extents(text)
        context.move_to((width - extents.width) / 2.0, height - (height - extents.height) / 2.0)
        context.show_text(text)
        return (width, extents.height*1.2)

class DigitalClock(Text):
    def __init__(self, width_percent=50):
        super().__init__(width_percent)
    
    def get_text(self): 
        return datetime.datetime.now().strftime("%H:%M")
    

        
        
class Date(Text):
    def __init__(self, width_percent=80):
        super().__init__(width_percent)
    
    def get_text(self): 
        return datetime.datetime.now().strftime("%A, %-d %B %Y")