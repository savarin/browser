import collections
from typing import Dict, List, Union

AttrMap = Dict[str, str]

Text = str
ElementData = collections.namedtuple("ElementData", ["tag_name", "attributes"])

NodeType = Union[Text, ElementData]


class Node():
    def __init__(self, children, node_type):
        # type: (List[Node], NodeType) -> None
        """
        """
        # data common to all nodes
        self.children = children

        # data specific to each node type
        self.node_type = node_type


def text(data):
    # type: (str) -> Node
    """
    """
    return Node(
        children=[],
        node_type=data,
    )


def elem(name, attrs, children):
    # type: (str, AttrMap, List[Node]) -> Node
    """
    """
    return Node(
        children=children,
        node_type=ElementData(
            tag_name=name,
            attributes=attrs,
        )
    )
