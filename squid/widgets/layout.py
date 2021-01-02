from squid.widgets.base import Component

class ChildInfo:
    def __init__(self, child, expand=False):
        self.child = child
        self.expand = expand
        self.used_space = (0, 0)
  

class Container(Component):
    def __init__(self):
        self._children = []
   
    def add_child(self, child, expand=False):
        self._children.append(ChildInfo(child, expand))
        
    def draw(self, context, width, height):
        context.save()
        context.rectangle(0, 0, width, height)
        context.clip()
        self.draw_children(context, width, height)
        context.restore()
        
    def draw_children(self, context, width, height):
        raise Exception("Unimplemented")
        
class HBox(Container):
    def __init__(self):
        super().__init__()
        
    def draw_children(self, context, parent_width, parent_height):
        free_space = parent_height
        expand_count = 0
        for node in self._children:
            if node.expand: expand_count += 1
            context.save()
            node.used_space = node.child.get_used_size(context, parent_width, parent_height)
            context.restore()
            free_space -= node.used_space[1]
        
        expand_space = 0
        expand_all = False
        if expand_count == 0: 
            expand_count = len(self._children)
            expand_all = True
        if free_space > 0 and expand_count > 0:
            expand_space = free_space / (expand_count - 1)

        total_y = 0
        for node in self._children:
            width = node.used_space[0]
            height = node.used_space[1]
            
            x = (parent_width - width) / 2.0
            y = 0
            if node.expand or expand_all: 
                y += expand_space / 2.0

            context.save()
            context.translate(x, total_y + y)
            context.rectangle(0, 0, width, height)
            context.clip()
            node.used_space = node.child.draw(context, width, height)
            total_y += y + node.used_space[1]
            context.restore()
            
        
class Stack(Container):
    def __init__(self):
        super().__init__()
        
    def draw_children(self, context, width, height):
        for node in self._children:
            context.save()
            context.rectangle(0, 0, width, height)
            context.clip()
            node.child.draw(context, width, height)
            context.restore()
