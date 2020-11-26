import heapq


class Dijkstra(object):

    @staticmethod
    def compute(network, start):
        start.set_weight(0)

        # create the priority queue with nodes
        unvisited_queue = [(node.get_weight(), node) for node in network]
        heapq.heapify(unvisited_queue)

        while len(unvisited_queue):
            # pop a node with the smallest distance
            unvisited_node = heapq.heappop(unvisited_queue)
            current_node = unvisited_node[1]
            current_node.set_visited()

            for next_node in current_node.connected_nodes:
                if not next_node.visited:
                    new_weight = current_node.get_weight() + \
                                 current_node.get_neighbor_weight(next_node)
                    if new_weight < next_node.get_weight():
                        next_node.set_weight(new_weight)
                        next_node.set_previous(current_node)

            # Rebuild heap: Pop every item, Put all nodes not visited into the queue
            while len(unvisited_queue):
                heapq.heappop(unvisited_queue)
            unvisited_queue = [(n.get_weight(), n) for n in network if not n.visited]
            heapq.heapify(unvisited_queue)

    @staticmethod
    def compute_shortest_path(node, path):
        if node.previous:
            path.append(node.previous.get_name())
            Dijkstra.compute_shortest_path(node.previous, path)
