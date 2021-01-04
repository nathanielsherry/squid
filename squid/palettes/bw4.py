light_tone_lut = [0xff, 0xc0, 0x80, 0x00]
dark_tone_lut = light_tone_lut[:]
dark_tone_lut.reverse()
tone_lut = light_tone_lut

def set_tone(context, value):
    if value == 0:
        context.set_source_rgba(0, 0, 0, 0.0)
    else:    
        shade = tone_lut[value-1]
        context.set_source_rgba(shade/255.0, shade/255.0, shade/255.0, 1.0)

def init(invert=False):
    global tone_lut
    tone_lut = dark_tone_lut if invert else light_tone_lut

