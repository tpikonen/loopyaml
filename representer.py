import math
from yaml.representer import *
from yaml.nodes import *
from loopsequence import *
from loopdict import *

class ColumnSequence(list):
    def __init__(self, sequence=[], ncols=1):
        list.__init__(self)
        self.extend(sequence)
        self.ncols = ncols


def represent_columnsequence(self, colseq, flow_style=True):
    tag = u'tag:yaml.org,2002:seq'
    value = []
    node = LoopSequenceNode(tag, value, colseq.ncols, flow_style=flow_style)
    if self.alias_key is not None:
        self.represented_objects[self.alias_key] = node
    best_style = True
    for item in colseq:
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


def prepare_mappingnode(self, mapping, flow_style=False):
    tag = u'tag:yaml.org,2002:map'
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
    return node, value


def represent_loopdict(self, data, flow_style=False):
    """PyYAML representer for the Loopdict type."""
    ## self is the yaml.Representer object

    # Prepare a dict without loopvars or attributes
    dnorm = data.copy()
    for loop in data.loops:
        for k in loop[0]:
            dnorm.pop(k, None) # None because of possible duplicates
            for att in loop[1]:
                dnorm.pop(k+att, None)
    # Output the reduced dict
    mapping = dnorm
    node, value = prepare_mappingnode(self, mapping)
    # Output loops
    # FIXME: check if '=loops=' key exists in dict
    loops_key = self.represent_data('=loops=')
    lseq = []
    for loop in data.loops:
        cols = list(loop[0]) # New copy to avoid YAML references
        lmap = {'$cols' : cols }
        for att in loop[1]:
            attlist = []
            for k in loop[0]:
                attlist.append(data.get(k+att))
            lmap['+'+att] = attlist
        valseq = []
        for i in range(len(data[loop[0][0]])):
            for k in loop[0]:
                valseq.append(data[k][i])
        lmap['~vals'] = ColumnSequence(valseq, len(loop[0]))
        lseq.append(lmap)
    value.append((loops_key, self.represent_data(lseq)))
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
LoopRepresenter.add_representer(ColumnSequence,
        represent_columnsequence)
LoopRepresenter.add_representer(Loopdict,
        represent_loopdict)
