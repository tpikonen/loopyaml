from yaml.events import *
from yaml.nodes import *

class LoopSequenceStartEvent(SequenceStartEvent):
    def __init__(self, anchor, tag, implicit, columns, **kwargs):
        self.columns = columns
        SequenceStartEvent.__init__(self, anchor, tag, implicit, **kwargs)

class LoopSequenceEndEvent(SequenceEndEvent):
    pass

class LoopSequenceNode(SequenceNode):
    id = 'loopsequence'
    def __init__(self, tag, value, columns, **kwargs):
        self.columns = columns
        SequenceNode.__init__(self, tag, value, **kwargs)

