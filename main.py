
from algorithms.shortest_path import Dijkstra
from graph.network import Network


def read_network_from_file(file_name, delimeter=','):
    """ Read from a file and build a network
    file_name: file to read from
    delimeter: delimeter that separates fields
    """
    cities = list()
    distances = dict()

    f = open(file_name, 'r')
    lines = f.readlines()
    for line in lines:
        fields = line.rstrip().split(delimeter)
        city_1 = fields[0].strip(' ')
        city_2 = fields[1].strip(' ')
        distance = float(fields[2])

        # build the list of cities
        if city_1 not in cities:
            cities.append(city_1)
        if city_2 not in cities:
            cities.append(city_2)

        # build the dictionary based on city distances
        if cities.index(city_1) not in distances.keys():
            distances[cities.index(city_1)] = {cities.index(city_2): distance}
        if cities.index(city_2) not in distances[cities.index(city_1)].keys():
            distances[cities.index(city_1)][cities.index(city_2)] = distance

    return cities, distances


def main():
    # application salutation
    application_name = 'Network Analysis'
    print('-' * len(application_name))
    print(application_name)
    print('-' * len(application_name))

    # read network from file
    file_name = 'data/unique_routes.csv'
    cities, distances = read_network_from_file(file_name)

    # build the network
    network = Network()
    network.add_nodes(cities)
    for connection in distances.items():
        frm = cities[connection[0]]
        for connection_to in connection[1].items():
            network.add_edge(frm, cities[connection_to[0]], connection_to[1])

    # uncomment to print the network
    # print(network)

    # get from user the start city
    for (index, city) in enumerate(network.get_nodes()):
        print(f'{index}: {city:s}')
    start_city_index = int(input(
        f'What is the start city by index (0 to {len(network.get_nodes()) - 1})? '))
    start_city = network.get_nodes()[start_city_index]

    # using Dijkstra's algorithm, compute least cost (distance)
    # from start city to all other cities
    Dijkstra.compute(network, network.get_node(start_city))

    # show the shortest path(s) from start city to all other cities
    print('\nShortest Paths')
    for target_node in network.get_nodes():
        target_city = network.get_node(target_node)
        path = [target_city.get_name()]
        Dijkstra.compute_shortest_path(target_city, path)
        print(f'{start_city} -> {target_node} = {path[::-1]} : {target_city.get_weight()}')
#%%

def get_path_distance(start_city, target_city):

    # read network from file
    file_name = 'data/unique_routes.csv'
    cities, distances = read_network_from_file(file_name)

    # build the network
    network = Network()
    network.add_nodes(cities)
    for connection in distances.items():
        frm = cities[connection[0]]
        for connection_to in connection[1].items():
            network.add_edge(frm, cities[connection_to[0]], connection_to[1])

    # using Dijkstra's algorithm, compute least cost (distance)

    Dijkstra.compute(network, network.get_node(start_city))

    target_city = network.get_node(target_city)
    path = [target_city.get_name()]
    Dijkstra.compute_shortest_path(target_city, path)
#print(f'{start_city} -> {target_city} = {path[::-1]} : {target_city.get_weight()}')

    path = f'{path[::-1]}'
    distance = f'{target_city.get_weight()}'
    
    return path, distance
        

#%%

# =============================================================================
# if __name__ == '__main__':
#     main()
# =============================================================================
