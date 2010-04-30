from yaml.serializer import *
from yaml.nodes import *
from yaml.events import *
from loopsequence import *


class LoopSerializer(Serializer):
    def serialize_node(self, node, parent, index):
        alias = self.anchors[node]
        if node in self.serialized_nodes:
            self.emit(AliasEvent(alias))
        else:
            self.serialized_nodes[node] = True
            self.descend_resolver(parent, index)
            if isinstance(node, ScalarNode):
                detected_tag = self.resolve(ScalarNode, node.value, (True, False))
                default_tag = self.resolve(ScalarNode, node.value, (False, True))
                implicit = (node.tag == detected_tag), (node.tag == default_tag)
                self.emit(ScalarEvent(alias, node.tag, implicit, node.value,
                    style=node.style))
            elif isinstance(node, LoopSequenceNode):
                implicit = (node.tag
                            == self.resolve(LoopSequenceNode, node.value, True))
                self.emit(LoopSequenceStartEvent(alias, node.tag, implicit,
                    node.columns, flow_style=node.flow_style))
                index = 0
                for item in node.value:
                    self.serialize_node(item, node, index)
                    index += 1
                self.emit(LoopSequenceEndEvent())
            elif isinstance(node, SequenceNode):
                implicit = (node.tag
                            == self.resolve(SequenceNode, node.value, True))
                self.emit(SequenceStartEvent(alias, node.tag, implicit,
                    flow_style=node.flow_style))
                index = 0
                for item in node.value:
                    self.serialize_node(item, node, index)
                    index += 1
                self.emit(SequenceEndEvent())
            elif isinstance(node, MappingNode):
                implicit = (node.tag
                            == self.resolve(MappingNode, node.value, True))
                self.emit(MappingStartEvent(alias, node.tag, implicit,
                    flow_style=node.flow_style))
                for key, value in node.value:
                    self.serialize_node(key, node, None)
                    self.serialize_node(value, node, key)
                self.emit(MappingEndEvent())
            self.ascend_resolver()
