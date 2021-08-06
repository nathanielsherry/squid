

_widget_classes = {}

def register(name, cls):
    global _widget_classes
    _widget_classes[name] = cls
    
def lookup(name):
    return _widget_classes.get(name, None)
