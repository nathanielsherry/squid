from squid.widgets.base import Component

light_tone_lut = [1.0, 0.66, 0.33, 0.0]
dark_tone_lut = [0.0, 0.33, 0.66, 1.0]
tone_lut = light_tone_lut

def set_tone(context, value):
    if value == 0:
        context.set_source_rgba(0, 0, 0, 0.0)
    else:    
        shade = tone_lut[value-1]
        context.set_source_rgba(shade, shade, shade, 1.0)

def init(invert=False):
    global tone_lut
    tone_lut = dark_tone_lut if invert else light_tone_lut

