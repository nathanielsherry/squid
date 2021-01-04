class Component:
    def __init__(self):
        pass
    
    def get_used_size(self, context, width, height): 
         raise Exception("Unimplemented")
    
    def draw(self, context, width, height):
        raise Exception("Unimplemented")
        
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
        from squid.palettes import set_tone
        set_tone(context, 4)
        text = self.get_text()
        context.set_font_size(self.calc_font_size(context, width, height))
        extents = context.text_extents(text)
        text_width = extents.width + extents.x_bearing
        context.move_to((width - text_width) / 2.0, height - (height - extents.height) / 2.0)
        context.show_text(text)
        return (width, extents.height*1.2)
