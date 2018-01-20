from floor_map import FloorMap
from database import *

store = find_store('coop')
start = get_start_node()
if start is not None:


# store_map = FloorMap()

# store_map.add_node('A', (100,100))
# store_map.add_node('B', (200,100), ['A'])
# store_map.add_node('C', (100,200), ['A'])
# store_map.add_node('D', (200,200), ['B', 'C'])
# store_map.add_node('E', (100,300), ['C'])
# store_map.add_node('F', (200,300), ['D', 'E'])

# store_map.add_node('Start', (79,127), ['A'])
# store_map.add_node('Goal', (200, 290), ['D', 'F'])

# # store_map.print_map()

# path = store_map.find_path('Start', 'Goal')
# print(path)