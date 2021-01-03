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
        if not child: raise Exception("Invalid Child {}".format(child))
        self._children.append(ChildInfo(child, expand))
        
    def get_used_size(self, context, width, height): 
        maxx = 0
        maxy = 0
        for node in self._children:
            cx, cy = node.child.get_used_size(context, width, height)
            maxx = max(cx, maxx)
            maxy = max(cy, maxy)
        return (maxx, maxy)
                       
class HBox(Container):
    def __init__(self):
        super().__init__()
            
    def draw(self, context, parent_width, parent_height):
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
            if not node.used_space: raise Exception("Component {} returned None for used space".format(node.child))
            total_y += y + node.used_space[1]
            context.restore()
            
        return (parent_width, total_y)
            
    @staticmethod
    def build(*args):
        s = HBox()
        for arg in args:
            s.add_child(arg)
        return s
    
        
class Stack(Container):
    def __init__(self):
        super().__init__()
        
    def draw(self, context, width, height):
        maxx = 0
        maxy = 0
        for node in self._children:
            context.save()
            context.rectangle(0, 0, width, height)
            context.clip()
            cx, cy = node.child.draw(context, width, height)
            maxx = max(cx, maxx)
            maxy = max(cy, maxy)
            context.restore()
            
        return (maxx, maxy)
        
    @staticmethod
    def build(*args):
        s = Stack()
        for arg in args:
            s.add_child(arg)
        return s
