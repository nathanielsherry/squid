import yaml
from squid.widgets.registry import lookup

from squid.widgets import base, clock, decor, layout

def load(filename):
    with open(filename, 'r') as h: contents = h.read()
    return yaml.safe_load(contents)
    
def build(arg):
    if isinstance(arg, list): 
        return [build(a) for a in arg]
    elif isinstance(arg, dict):
        if not 'node' in arg:
            return {k: build(v) for k, v in arg.items()}
        else:
            node = arg['node']
            
            constructor = None
            parent_args = {}
            if isinstance(node, str):
                constructor = lookup(node)
            else:
                constructor = lookup(node['name'])
                parent_args = node.copy()
                del parent_args['name']
            
            widget_args = arg.copy()
            del widget_args['node']
            widget_args = {k: build(v) for k, v in widget_args.items()}

            widget = constructor(**widget_args)
            widget.set_parent_args(parent_args)
            return widget

    else:
        return arg

    
        
