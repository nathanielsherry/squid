class Component:
    def __init__(self):
        pass
    
    @property
    def min_width(self): return 0

    @property
    def min_height(self): return 0

    def get_used_size(self, context, width, height): 
        return (width, height)
    
    def draw(self, context, width, height):
        raise Exception("Unimplemented")
