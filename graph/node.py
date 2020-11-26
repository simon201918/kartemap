class Node(object):

    def __init__(self, name):
        self.name = name
        self.connected_nodes = {}
        self.weight = float('inf')
        self.visited = False
        self.previous = None

    def get_name(self):
        return self.name

    def add_connection(self, neighbor, weight=0):
        self.connected_nodes[neighbor] = weight

    def get_connections(self):
        return self.connected_nodes.keys()

    def get_neighbor_weight(self, neighbor):
        return self.connected_nodes[neighbor]

    def set_weight(self, weight):
        self.weight = weight

    def get_weight(self):
        return self.weight

    def set_previous(self, previous):
        self.previous = previous

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return f'{self.name}: {[x.name for x in self.connected_nodes]}'

    def __lt__(self, other):
        return self.weight < other.weight
