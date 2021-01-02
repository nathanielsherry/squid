from squid.widgets.base import Component

light_tone_lut = [1.0, 0.66, 0.33, 0.0]
dark_tone_lut = [0.0, 0.33, 0.66, 1.0]
tone_lut = light_tone_lut

def set_tone(context, value):
    shade = tone_lut[value-1]
    context.set_source_rgba(shade, shade, shade, 1.0)

def init(invert=False):
    global tone_lut
    tone_lut = dark_tone_lut if invert else light_tone_lut


class FloodFill(Component):
    def __init__(self, tone):
        super().__init__()
        self._tone = tone
        
    def draw(self, context, width, height):
        set_tone(context, self._tone)
        context.paint()
        
