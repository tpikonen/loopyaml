from yaml.dumper import *
from yaml.representer import *
from yaml.resolver import *
from emitter import *
from serializer import *
from loopdict import *


def represent_loopsequence(self, tag, sequence, columns, flow_style=True):
    value = []
    node = LoopSequenceNode(tag, value, columns, flow_style=flow_style)
    if self.alias_key is not None:
        self.represented_objects[self.alias_key] = node
    best_style = True
    for item in sequence:
        node_item = self.represent_data(item)
        if not (isinstance(node_item, ScalarNode) and not node_item.style):
            best_style = False
        value.append(node_item)
    if flow_style is None:
        if self.default_flow_style is not None:
            node.flow_style = self.default_flow_style
        else:
            node.flow_style = best_style
    return node


def loopdict_representer(self, data, flow_style=False):
    """PyYAML representer for the Loopdict type."""
    # self is the yaml.Representer object
    dnorm = data.copy()
    dloop = {}
    for k in data.loopvars:
        dloop[k] = dnorm.pop(k)
    tag = u'tag:yaml.org,2002:map'
    mapping = dnorm
    # copypaste from represent_mapping
    value = []
    node = MappingNode(tag, value, flow_style=flow_style)
    if self.alias_key is not None:
        self.represented_objects[self.alias_key] = node
    best_style = True
    if hasattr(mapping, 'items'):
        mapping = mapping.items()
        mapping.sort()
    for item_key, item_value in mapping:
        node_key = self.represent_data(item_key)
        node_value = self.represent_data(item_value)
        if not (isinstance(node_key, ScalarNode) and not node_key.style):
            best_style = False
        if not (isinstance(node_value, ScalarNode) and not node_value.style):
            best_style = False
        value.append((node_key, node_value))
    if flow_style is None:
        if self.default_flow_style is not None:
            node.flow_style = self.default_flow_style
        else:
            node.flow_style = best_style
    # copypaste ends
    vars_key = self.represent_data('=cols')
    vars_item = self.represent_data(data.loopvars)
    value.append((vars_key, vars_item))
    loopseq = []
    for i in range(len(data[data.loopvars[0]])):
        for k in data.loopvars:
            loopseq.append(data[k][i])
    loop_key = self.represent_data('=loop')
    loop_item = represent_loopsequence(self, u'tag:yaml.org,2002:seq', loopseq,
            len(data.loopvars))
    value.append((loop_key, loop_item))

    return node


class LoopDumper(LoopEmitter, LoopSerializer, Representer, Resolver):

    def __init__(self, stream,
            default_style=None, default_flow_style=None,
            canonical=None, indent=None, width=None,
            allow_unicode=None, line_break=None,
            encoding=None, explicit_start=None, explicit_end=None,
            version=None, tags=None):
        LoopEmitter.__init__(self, stream, canonical=canonical,
                indent=indent, width=width,
                allow_unicode=allow_unicode, line_break=line_break)
        LoopSerializer.__init__(self, encoding=encoding,
                explicit_start=explicit_start, explicit_end=explicit_end,
                version=version, tags=tags)
        Representer.__init__(self, default_style=default_style,
                default_flow_style=default_flow_style)
        Resolver.__init__(self)
        self.add_representer(Loopdict, loopdict_representer)
