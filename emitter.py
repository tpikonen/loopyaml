from yaml.emitter import *
from yaml.error import YAMLError
from yaml.events import *
from loopsequence import *


class LoopEmitter(Emitter):
    def __init__(self, stream, **kwargs):
        self.loopcolumns = None
        self.curloopcol = None
        Emitter.__init__(self, stream, **kwargs)

    # Node handler with LoopSequence support
    def expect_node(self, root=False, loopsequence=False, sequence=False,
            mapping=False, simple_key=False):
        self.root_context = root
        self.loopsequence_context = loopsequence
        self.sequence_context = sequence
        self.mapping_context = mapping
        self.simple_key_context = simple_key
        if isinstance(self.event, AliasEvent):
            self.expect_alias()
        elif isinstance(self.event, (ScalarEvent, CollectionStartEvent)):
            self.process_anchor(u'&')
            self.process_tag()
            if isinstance(self.event, ScalarEvent):
                self.expect_scalar()
            elif isinstance(self.event, LoopSequenceStartEvent):
                if self.flow_level or self.canonical or self.event.flow_style   \
                        or self.check_empty_sequence():
                    self.expect_flow_loopsequence(self.event.columns)
                else:
                    self.expect_block_sequence()
            elif isinstance(self.event, SequenceStartEvent):
                if self.flow_level or self.canonical or self.event.flow_style   \
                        or self.check_empty_sequence():
                    self.expect_flow_sequence()
                else:
                    self.expect_block_sequence()
            elif isinstance(self.event, MappingStartEvent):
                if self.flow_level or self.canonical or self.event.flow_style   \
                        or self.check_empty_mapping():
                    self.expect_flow_mapping()
                else:
                    self.expect_block_mapping()
        else:
            raise EmitterError("expected NodeEvent, but got %s" % self.event)

    # Flow loopsequence handlers.

    def expect_flow_loopsequence(self, columns):
        self.write_indicator(u'[', True, whitespace=True)
        self.flow_level += 1
        self.increase_indent(flow=True)
        self.write_indent()
        self.state = self.expect_first_flow_loopsequence_item
        self.loopcolumns = columns
        self.curloopcol = 0

    def expect_first_flow_loopsequence_item(self):
        if isinstance(self.event, LoopSequenceEndEvent):
            self.indent = self.indents.pop()
            self.flow_level -= 1
            self.write_indicator(u']', False)
            self.state = self.states.pop()
            self.loopcolumns = None
            self.curloopcol = None
        else:
            if self.canonical or self.column >= self.best_width:
                self.write_indent()
            self.states.append(self.expect_flow_loopsequence_item)
            self.expect_node(loopsequence=True)

    def expect_flow_loopsequence_item(self):
        if isinstance(self.event, LoopSequenceEndEvent):
            self.indent = self.indents.pop()
            self.flow_level -= 1
            if True: #self.canonical:
                self.write_indicator(u',', False)
                self.write_indent()
            self.write_indicator(u']', False)
            self.state = self.states.pop()
            self.loopcolumns = None
            self.curloopcol = None
        else:
            self.write_indicator(u',', False)
            self.curloopcol += 1
            if self.canonical or self.curloopcol >= self.loopcolumns:
                self.write_indent()
                self.curloopcol = 0
            self.states.append(self.expect_flow_loopsequence_item)
            self.expect_node(loopsequence=True)
