from graph.node import Node


class Network(object):

    def __init__(self):
        self.node_dict = {}
        self.num_nodes = len(self.node_dict)
        self.previous = None

    def __iter__(self):
        return iter(self.node_dict.values())

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        self.node_dict[node] = Node(node)
        self.num_nodes = len(self.node_dict)
        return self.node_dict[node]

    def get_node(self, n):
        return self.node_dict[n] if n in self.node_dict else None

    def add_edge(self, frm, to, weight=0.0):
        if frm not in self.node_dict:
            self.add_node(frm)
        if to not in self.node_dict:
            self.add_node(to)

        self.node_dict[frm].add_connection(self.node_dict[to], weight)
        self.node_dict[to].add_connection(self.node_dict[frm], weight)

    def get_nodes(self):
        return list(self.node_dict.keys())

    def set_previous(self, current):
        self.previous = current

    def get_previous(self):
        return self.previous

    def __str__(self):
        text = '\nNetwork\n'
        for node in self:
            for connected_node in node.get_connections():
                node_name = node.get_name()
                connected_node_name = connected_node.get_name()
                text += f'{node_name} -> {connected_node_name} :' \
                        f' {node.get_neighbor_weight(connected_node)}\n'
        return text
