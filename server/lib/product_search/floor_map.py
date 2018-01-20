from bson.objectid import ObjectId
import numpy as np
import queue


def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def abs_diff(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return (abs(x1-x2), abs(y1-y2))

def nearest_two_along_axis(nodes, pos, axis):
    nodes.sort(key=lambda x: abs(x.pos[axis] - pos[axis]))
    return nodes[:2]


class Node():
    def __init__(self, position, links, name):
        self.pos = position
        self.links = links
        self.name = name


class FloorMap():
    def __init__(self):
        self.nodes = {}

    def __str__(self):
        return str(self.nodes)

    def add_node(self, name, position, links=[], bidirectional=False):

        # deal with possible ObjectId names
        name = str(name)
        links = [str(l) for l in links]

        node = Node(position, links, name)
        self.nodes[name] = node

        if bidirectional:
            for link in links:
                if link in self.nodes:
                    self.nodes[link].links.append(name)
                else:
                    raise ValueError(
                        "The node \"%s\" in links does not exist" % str(link))

    def get_graph(self):
        return self.nodes


    def find_closest_edge(self, pos):  # O(N)
        # find the edge with the smallest perpendicular distance to pos
        # currently assumes all nodes are either horizontal or vertical
        # returns the two nodes of the edge

        xmin = np.inf
        xmin_nodes = []
        ymin = np.inf
        ymin_nodes = []

        for name in self.nodes:
            x, y = abs_diff(self.nodes[name].pos, pos)
            if x <= xmin:
                xmin = x
                xmin_nodes.append(self.nodes[name])
            if y <= ymin:
                ymin = y
                ymin_nodes.append(self.nodes[name])
        
        if xmin < ymin:
            return nearest_two_along_axis(xmin_nodes, pos, 0)
        else:
            return nearest_two_along_axis(ymin_nodes, pos, 1)


    def find_path(self, start, goal):

        frontier = queue.PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            if current not in self.nodes:
                raise ValueError("The node \"%s\" is not in the map" % current)

            for link_node in self.nodes[current].links:
                cost = distance(self.nodes[current].pos,
                                self.nodes[link_node].pos)

                new_cost = cost_so_far[current] + cost
                if link_node not in cost_so_far or new_cost < cost_so_far[link_node]:
                    cost_so_far[link_node] = new_cost
                    priority = new_cost
                    frontier.put(link_node, priority)
                    came_from[link_node] = current

        path = []
        current = goal
        while current is not None:
            path.append(self.nodes[current].pos)
            current = came_from[current]
        path = np.array(path[::-1])

        return path

    def print_map(self):
        print('\nMap Graph:')
        for node in self.nodes:
            print('%s %s %s' % (node, self.nodes[node].pos,
                                self.nodes[node].links))
        print()
