from squid.widgets.base import Component
from squid.palettes import set_tone
import math

class Notches(Component):
    def __init__(self, size, tone):
        self._size = size
        self._tone = tone

    def get_used_size(self, context, width, height):
        return (width, self._size)
    
    def draw(self, context, width, height):
        set_tone(context, self._tone)
        size = min(width, height)
        size = self._size / 100 * size
        
        def notch(rot):
            
            context.translate(width/2, height/2)
            context.rotate(rot)
            context.translate(-width/2, -height/2)
            
            #left
            context.move_to(0, 0)
            context.line_to(size, 0)
            context.line_to(0, size)
            context.close_path()
            context.fill()
            
            #right
            context.move_to(width, 0)
            context.line_to(width, size)
            context.line_to(width-size, 0)
            context.close_path()
            context.fill()
        
        notch(0)
        notch(math.pi)

        return (width, self._size)
    
class FloodFill(Component):
    def __init__(self, tone):
        super().__init__()
        self._tone = tone
    
    def get_used_size(self, context, width, height): 
        return (width, height)
    
    def draw(self, context, width, height):
        set_tone(context, self._tone)
        context.paint()
        return (width, height)
        
#Accepts
# * size of border, as percent of minor axis
# * tone value for filling the border
# * inner component to draw in the remaining space
class Border(Component):
    def __init__(self, size, tone, inner, inner_tone=0):
        self._inner = inner
        self._tone = tone
        self._size = size
        self._inner_tone = inner_tone
        
    def get_used_size(self, context, width, height): 
         return self._inner.get_used_size(context, width, height)
    
    def draw(self, context, width, height):
        size = min(width, height)
        bw = size * self._size / 100
        bh = bw
        
        #draw the border
        context.save()
        self.border_path(context, width, height)
        if self._inner_tone != 0:
            set_tone(context, self._inner_tone)
            context.fill_preserve()
        context.set_line_width(bw)
        set_tone(context, self._tone)
        context.stroke()
        context.restore()
        
        #draw the inner component
        iw, ih, = width-2*bw, height-2*bw
        context.save()
        context.translate(bw, bh)
        self._inner.draw(context, iw, ih)
        context.restore()
        
        return (width, height)
        
    def border_path(self, context, width, height):
        size = min(width, height)
        bw = self._size * size / 100
        bwmid = bw/2.0
        
        w1 = bwmid
        w2 = width - w1
        
        h1 = bwmid
        h2 = height - h1        
        
        context.move_to(w1, h1)
        context.line_to(w2, h1)
        context.line_to(w2, h2)
        context.line_to(w1, h2)
        context.close_path()
        
        
class NotchedBorder(Border):
    def __init__(self, size, tone, notch_size, inner, inner_tone=0):
        super().__init__(size, tone, inner, inner_tone)
        self._notch_size = notch_size
        
    def border_path(self, context, width, height):
        size = min(width, height)
        bw = self._size * size / 100
        bwmid = bw/2.0
        nw = self._notch_size * size / 100
        
        w1 = bwmid
        w2 = nw
        w3 = width - w2
        w4 = width - w1
        
        h1 = bwmid
        h2 = nw
        h3 = height - h2
        h4 = height - h1
        
        
        #start top center, corners come in pairs
        context.move_to(width/2, bwmid)
        #top right
        context.line_to(w3, h1)
        context.line_to(w4, h2)
        #bottom right
        context.line_to(w4, h3)
        context.line_to(w3, h4)
        #bottom left
        context.line_to(w2, h4)
        context.line_to(w1, h3)
        #top left
        context.line_to(w1, h2)
        context.line_to(w2, h1)
        
        context.close_path()
        
