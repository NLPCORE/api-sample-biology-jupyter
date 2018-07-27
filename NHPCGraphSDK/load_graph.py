from .link_representation import load_link, Link
from .node_representation import Node


class Graph:
    __nodes__ = None  # type: list[Node]

    def __init__(self):
        self.__nodes__ = []
        self.__nodes_id_map__ = {}

        self.__links__ = []
        self.__link_id_map__ = {}

    def get_nodes(self) -> Node:
        for node in self.__nodes__:
            yield node

    def get_links(self) -> Link:
        for link in self.__links__:
            yield link

    def node_by_id(self, node_id) -> Node:
        return self.__nodes_id_map__[node_id]

    def get_link_by_id(self, link_id) -> Link:
        return self.__link_id_map__[link_id]

    def get_nodes_with_attribute(self, attribute_name) -> Node:
        for node in self.__nodes__:
            if node.has_attribute(attribute_name):
                yield node

    def get_node_with_group_type(self, group_name) -> Node:
        for node in self.__nodes__:
            if node.is_group_type(group_name):
                yield node

    def load_graph(self, graph_obj):
        nodes_id_map = {}

        def add_node_id(node_id, link_id):
            nodes_id_map.update({str(node_id): nodes_id_map.get(node_id, []) + [link_id]})

        for link_id, link_obj in graph_obj['links'].items():
            link = load_link(link_obj, self)
            self.__links__.append(link)
            self.__link_id_map__[link_id] = link
            add_node_id(link_obj['source'], link)
            add_node_id(link_obj['target'], link)
        for node_id, node_obj in graph_obj['nodes'].items():
            node = Node.from_object(node_obj, link_ids=nodes_id_map.get(node_id, []))
            self.__nodes__.append(node)
            self.__nodes_id_map__[node_id] = node_obj


def load_graph(graph_obj) -> Graph:
    graph = Graph()
    graph.load_graph(graph_obj)
    return graph
