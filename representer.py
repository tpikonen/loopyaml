import math
from yaml.representer import *
from yaml.nodes import *
from loopsequence import *

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
    attkeys = data.attributes
    attdict = {}
    for att in attkeys:
        attvals = []
        for k in data.loopvars:
            attvals.append(dnorm.pop(k+att, None))
        attdict[att] = attvals
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
    for att in attkeys:
        akey = self.represent_data('='+att)
        aval = self.represent_data(attdict[att])
        value.append((akey, aval))
    loopseq = []
    for i in range(len(data[data.loopvars[0]])):
        for k in data.loopvars:
            loopseq.append(data[k][i])
    loop_key = self.represent_data('=loop')
    loop_item = represent_loopsequence(self, u'tag:yaml.org,2002:seq', loopseq,
            len(data.loopvars))
    value.append((loop_key, loop_item))

    return node


class LoopRepresenter(Representer):
    def __init__(self, float_width=15, **kwargs):
        if float_width < 7:
            raise ValueError("Minimum width of the float field must be >= 7")
        self.float_width = float_width
        Representer.__init__(self, **kwargs)

    def represent_float(self, data):
        if math.isnan(data):
            value = u'.nan'
        elif data == self.inf_value:
            value = u'.inf'
        elif data == -self.inf_value:
            value = u'-.inf'
        else:
            #value = unicode(repr(data)).lower()
            value = u'%#0*.*e' % (self.float_width, self.float_width-5, data)
            # Note that in some cases `repr(data)` represents a float number
            # without the decimal parts.  For instance:
            #   >>> repr(1e17)
            #   '1e17'
            # Unfortunately, this is not a valid float representation according
            # to the definition of the `!!float` tag.  We fix this by adding
            # '.0' before the 'e' symbol.
            if u'.' not in value and u'e' in value:
                value = value.replace(u'e', u'.0e', 1)
        return self.represent_scalar(u'tag:yaml.org,2002:float', value)

LoopRepresenter.add_representer(float,
        LoopRepresenter.represent_float)
