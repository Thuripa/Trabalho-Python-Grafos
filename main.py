# ---------------------------------------------------------------------------- #

#                          Graph Assignment in Python                          #

# Guilherme Melo de Jesus

# Rômulo Pedro Thomsen


# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                             Imports and Variables                            #
# ---------------------------------------------------------------------------- #

import os
import platform
import classes.Graph as Graph
from collections import deque

LINUX = (platform.system() == "Linux")
WINDOWS = (platform.system() == "Windows")
DEBUG = True
if (WINDOWS):
	import msvcrt

if (LINUX):
	import sys
	import tty
	import termios


_graph = None # The current graph we have created.
_warning = "" # Warning message to be displayed, even after clearing console. 

# Common texts
_invalidOption = "Invalid Option."
_notImplemented = "Not implemented."
_selOption = "Select Option: "
_inputLabel = "Input vertex's label: "
_inputContinue = "Press any key to continue."


# ---------------------------------------------------------------------------- #
#                                    Methods                                   #
# ---------------------------------------------------------------------------- #

# Set the current warning
def set_warn(text):
	global _warning
	_warning = text

# Clears the warning
def clear_warn():
	global _warning
	_warning = ""

# Clears the console screen.
def clear():
	global _warning
	if WINDOWS:
		os.system('cls')
	if LINUX:
		os.system('clear')
	print(str(_warning))

# Asks for the user input of only a single character
def input_char(text):
	print(text, end="", flush=True)
	if WINDOWS:
		char = msvcrt.getch()
		print()
		return char.decode("utf-8").lower()
	if LINUX:
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			char = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
			print()
		return char.lower()
	# We're out of options. What are you using? Mac? TempleOS?
	return input(text)[0]

# Returns a numeric value, as a menu option.
def menu_input():
	_input = input_char(_selOption) 
	_opt = -1 # Default is -1.
	if (_input.isnumeric()):
		_opt = int(_input) # Pass to number if numeric
	if (_input.lower() == "q"):
		_opt = 0 # Convert Q to 0
	return _opt # Will return -1 if invalid input.

# Asks the user in a Y/N fashion, returns True or False.
def input_bool(text):
	# Ignore case.
	_input = input_char(text + " (Y/N): ").lower()

	# Y or N
	if (_input == "y"):
		return True
	elif(_input == "n"):
		return False

	# 0 or 1
	if (_input.isnumeric()):
		if (_input == 1):
			return True
		else:
			return False

	return False

def input_edge():
	_o = input_char("Origin Vertex: ")
	_origin = _graph.vertex_get(_o)
	# Check if origin vertex exists.
	if (_origin == None):
		set_warn(f"Vertex [{_o}] does not exist.")
		return None
	_d = input_char("Destination Vertex: ")
	_dest = _graph.vertex_get(_d)
	# Check if destination vertex exists
	if (_dest == None):
		set_warn(f"Vertex [{_d}] does not exist.")
		return None

	_edge = _graph.edge_get(_o, _d)
	_reciprocate = _graph.edge_get(_d, _o)

	# Return all the info. This can be used to create new edges or access existing.
	return [_origin, _dest, _edge, _reciprocate]

# Prints the adjacency matrix, being the graph Edge-Weighted or not, Directed or not.
def print_matrix():
	clear()
	_labels = []

	# Label sorting
	def _sort(e):
		return e.label

	_graph.vertices.sort(key=lambda x: x.label)

	# Horizontal Header
	for v in _graph.vertices:
		_labels.append(v.label)
	print("  " + " ".join(_labels))
	print(" ")

	# Line by line
	for v in _graph.vertices:
		_line = v.label + " "
		_nums = []
		for o in _graph.vertices:
			if (v == o):
				_nums.append("0")
				continue
			_num = 0
			_out = _graph.edge_get(v.label, o.label) # Outbound connection
			_in = _graph.edge_get(o.label, v.label) # Inbound connection

			if (_out is not None):
				_num += _out.weight
			if (_in is not None and not _graph.directional):
				_num += _in.weight
			_nums.append(str(_num))
		print(f"{v.label} " + " ".join(_nums))
		print(" ")

	
	input_char(_inputContinue)

# Prints the adjacency list, being the graph Edge-Weighted or not, Directed or not.
def print_list():
	clear()

	for v in _graph.vertices:
		_listing = []
		for e in _graph.edges:
			if (e.origin == v):
				if (_graph.weighted):
					_listing.append(f"({e.destination.label}-{str(e.weight)})")
				else:
					_listing.append(e.destination.label)
			if (e.destination == v and not _graph.directional):
				if (_graph.weighted):
					_listing.append(f"({e.origin.label}-{str(e.weight)})")
				else:
					_listing.append(e.origin.label)

		_s = ", ".join(_listing)
		print(f"[{v.label}] adjacent to [{_s}]")

	input_char(_inputContinue)

# Create a Directed Graph as show in reference.png
if DEBUG:
	_graph = Graph.Graph(False, True)
	_graph.vertex_add("1")
	_graph.vertex_add("2")
	_graph.vertex_add("3")
	_graph.vertex_add("4")
	_graph.vertex_add("5")
	_graph.edge_add("1", "2", 0)
	_graph.edge_add("2", "4", 0)
	_graph.edge_add("4", "1", 0)
	_graph.edge_add("4", "5", 0)
	_graph.edge_add("5", "3", 0)
	_graph.edge_add("3", "1", 0)


# ---------------------------------------------------------------------------- #
#                                     Menus                                    #
# ---------------------------------------------------------------------------- #

# --------------------------------- Main Menu -------------------------------- #
def menu():
	global _graphType
	clear()

	if (_graph == None):
		print("""
		# Main Menu
		[   1   ] - Create graph
		[ 0 / Q ] - Quit
		""")
	else:
		print("""
		# Main Menu
		[   1   ] - Create new graph
		[   2   ] - Edit existing Graph
		[ 0 / Q ] - Quit
		""")
	
	_opt = menu_input()

	match (_opt):
		case (1): # Create new graph
			clear_warn()
			while(True):
				if (menu_create_graph()):
					break
			return False
		case (2): # Edit graph
			# Only if graph exists.
			clear_warn()
			if (_graph == None):
				set_warn(_invalidOption)
				return False
			
			# Edit existing graph.
			while(True):
				if(menu_graph()):
					break
			return False
		case (0): # Quit
			clear_warn()
			return True
	set_warn(_invalidOption)
	return False

def menu_create_graph():
	global _graph
	clear()

	print("# Creating a Graph...")
	# Gather if its directional and/or weighted
	_weighted = input_bool("Weighted Graph?")
	_directional = input_bool("Directional?")
	print("Weighted: " + str(_weighted))
	print("Directional: " + str(_directional))
	_correct = input_bool("Is this correct?")

	if _correct:
		set_warn("Graph Created.")
		# Create Graph object
		_graph = Graph.Graph(_weighted, _directional)
		while(True):
			if (menu_graph()):
				return True
	set_warn("Please try again")
	return False

# ---------------------------- Graph Editing Menu ---------------------------- #
def menu_graph():
	clear()

	# This shouldn't happen!
	if (_graph == None):
		return True

	print("""
	# Graph Edit Menu
	[   1   ] - Vertex Options
	[   2   ] - Edges Options
	[   3   ] - Print List Graph
	[   4   ] - Print Matrix Graph
	[   5   ] - Show Neighbors
	[   6   ] - Deep First Search
	[   7   ] - Breadth First Search  
	[   8   ] - Dijkistra Transversal
	[ 0 / Q ] - Return to menu
	""")
	_opt = menu_input()

	match(_opt):
		case (1): # Vertex Options
			clear_warn()
			while(True):
				if (menu_vertex()):
					break
			return False
		case (2): # Edges Options
			clear_warn()
			while(True):
				if (menu_edges()):
					break
			return False
		case (3): # Print List Graph
			print_list()
			return False
		case (4): # Print Matrix Graph
			print_matrix()
			return False
		case (5): # Show Neighbors
			clear_warn()
			_label = input_char(_inputLabel)
			if (not _graph.vertex_exists(_label)):
				set_warn(f"Vertex [{_label}] does not exist.")
				return False

			_neighbors = _graph.vertex_get_neighbors(_label)
			if (_neighbors == None or _neighbors == []):
				set_warn(f"Vertex [{_label}] has no neighbors.")
				return False

			_string = f"Vertex [{_label}] has ["
			for i in range(0, len(_neighbors)):
				_last = (i == len(_neighbors)-1)
				_n = _neighbors[i]
				_string += _n.label
				if not _last:
					_string += ", "
			_string += "] as neighbors."

			set_warn(_string)
			return False
		case (6): # Deep First Search

			source = input("Insira o vértice de origem: ")
			print("DFS from source:", source)
			source = _graph.vertex_get(source)
			dfs(source)
	
			pass
		case (7): # Breath First Search
			# Mark all the vertices as not visited
			visited = [False] * len(_graph.vertices)

			# Perform BFS traversal starting from vertex 0
			source = input("Insira o vértice de origem: ")
			print("BFS starting from : "+source)
			source = _graph.vertex_get(source)
			bfs(source, visited)
		case (8): # Dijkistra
			# Perform Dijkistra traversal starting from vertex 'source'
			source = input("Insira o vértice de origem: ")
			print("Dijkistra starting from : "+source)
			source = _graph.vertex_get(source)
			dijkstra(source)	
		case (0):
			clear_warn()
			return True
			
	set_warn(_invalidOption)
	return False

# ---------------------------- Vertex Editing Menu --------------------------- #
def menu_vertex():
	clear()

	# This shouldn't happen!
	if (_graph == None):
		return True
	
	print("""
	# Vertex Menu
	[   1   ] - Insert Vertex
	[   2   ] - Remove Vertex
	[   3   ] - Label Vertex
	[   4   ] - List all Vertices
	[ 0 / Q ] - Return to menu
	""")
	_opt = menu_input()

	match(_opt):
		case (1): # Insert Vertex
			_label = input_char(_inputLabel)
			# Make sure a vertex with this name doesn't already exist.
			if (_graph.vertex_exists(_label)):
				set_warn("Vertex already exists.")
				return False
			# Tries to add the new vertex.
			if (_graph.vertex_add(_label)):
				set_warn("Vertex added.")
				return False
			set_warn("Something went wrong while adding the vertex.")
			return False
		case (2): # Remove Vertex
			_label = input_char(_inputLabel)
			# Checks if there even is a vertex with such a label
			if (not _graph.vertex_exists(_label)):
				set_warn("Vertex does not exist.")
			# Removes it, in case it really exists
			if (_graph.vertex_remove(_label)):
				set_warn("Vertex removed.")
				return False
			set_warn("Something went wrong while removing the vertex.")
			return False
		case (3): # Label Vertex
			_label = input_char(_inputLabel)
			# Checks if the vertex to rename exists.
			if (not _graph.vertex_exists(_label)):
				set_warn("Vertex does not exist.")
				return False
			_new = input_char("New label: ")
			# Check if there already is a vertex with the name we're trying to rename the current one to.
			if (_graph.vertex_exists(_new)):
				set_warn("There already exists a vertex with that label.")
				return False
			# Tries to rename the vertex safely.
			if (_graph.vertex_label(_label, _new)):
				set_warn("Vertex renamed.")
				return False
			set_warn("Something went wrong while renaming the vertex.")
			return False
		case (4): # List vertices
			set_warn(_graph.get_string_vertices())
			return False
		case (0): # Return
			clear_warn()
			return True

	set_warn(_invalidOption)
	return False

# ----------------------------- Edge Editing Menu ---------------------------- #
def menu_edges():
	clear()
	print("""
	# Edge Menu
	[   1   ] - Insert Edge
	[   2   ] - Remove Edge
	[   3   ] - Check if Edge exists
	[   4   ] - Show an Edge's weight
	[   5   ] - List all Edges.
	[ 0 / Q ] - Return to menu
	""")
	_opt = menu_input()

	match(_opt):
		case (1): # Insert Edge
			_info = input_edge()
			if (_info == None):
				return False
			_origin = _info[0]
			_dest = _info[1]
			_exists = (_info[2] != None)
			_reciprocate = (_info[3] != None)

			# If the edge already exists, don't add.
			if (_exists):
				set_warn("Edge already exists.")
				return False

			# If it's not directional, then if there's an reciprocate edge, its the same as this one
			if (not _graph.directional) and (_reciprocate):
				set_warn("Edge already exists: Graph is not directional.")
				return None

			# Get the weight, default is 1 for non-weighted graphs.
			_weight = 1
			if (_graph.weighted):
				_w = input("Weight: ")
				if (not _w.isnumeric()):
					set_warn("Invalid weight. Please try again.")
					return False
				_weight = int(_w)

			# Try to add the edge safely.
			if (_graph.edge_add(_origin.label, _dest.label, _weight)):
				set_warn("Edge added.")
				return False

			set_warn("Something went wrong while creating edge.")
			return False
		case (2): # Remove Edge
			_info = input_edge()
			if (_info == None):
				return False
			_origin = _info[0]
			_dest = _info[1]
			_exists = (_info[2] != None)
			_reciprocate = (_info[3] != None)

			# If we're in a directional context, the order matters.
			if (_graph.directional):
				if (_exists):
					if (_graph.edge_remove(_origin.label, _dest.label)):
						set_warn("Edge removed.")
						return False
			else:
				_rem = False
				if (_exists):
					if (_graph.edge_remove(_origin.label, _dest.label)):
						_rem = True
				if (_reciprocate):
					if (_graph.edge_remove(_dest.label, _origin.label)):
						_rem = True
				if (_rem):
					set_warn("Edge removed.")
					return False

			set_warn("Something went wrong while deleting the edge.")
			return False
		case (3): # Check if Edge exists
			_info = input_edge()
			if (_info == None):
				return False
			_exists = (_info[2] != None)
			_reciprocate = (_info[3] != None)

			if (_graph.directional):
				if (_exists):
					set_warn("Edge exists.")
				else:
					set_warn("Edge does not exist.")
			else:
				if (_exists or _reciprocate):
					set_warn("Edge exists.")
				else:
					set_warn("Edge does not exist.")

			return False
		case (4): # Show an Edge's weight
			if (not _graph.weighted):
				set_warn("Graph is not weighted.")
				return False

			_info = input_edge()
			if (_info == None):
				return False
			
			_edge = _info[2]
			_reci = _info[3]

			if (_edge != None):
				set_warn("Weight is: " + str(_edge.weight))
				return False
			if (not _graph.directional) and (_reci != None):
				set_warn("Weight is: " + str(_reci.weight))
				return False

			set_warn("Something went wrong while getting the edge's weights.")
			return False
		case (5): # List edges
			set_warn(_graph.get_string_edges())
			return False
		case (0): # Return
			clear_warn()
			return True

	set_warn(_invalidOption)
	return False

# Open a .txt file to create a Graph
def open_file():
	pass

# ----------------------------- Deep First Search ---------------------------- #
def dfs_rec(visited, source):
    # Mark the current vertex as visited
    visited[_graph.vertices.index(source)] = True

    # Print the current vertex
    print(source, end=" ")

    # Recursively visit all adjacent vertices
    # that are not visited yet
    for i in _graph.vertex_get_neighbors(source): # ERRO AKI <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        if not visited[i]:
            dfs_rec(visited, i)

def dfs(source):
    visited = [False] * len(_graph.vertices)
    # Call the recursive DFS function
    dfs_rec(visited, source)
# ---------------------------- ----------------- ------------------------------ #

# ---------------------------- Breadth First Search --------------------------- #
# Breadth First Search
def bfs(source, visited):
  
    # Create a queue for BFS
    q = deque()

    # Mark the source node as visited and enqueue it
    visited[_graph.vertices.index(source)] = True
    q.append(source)

    # Iterate over the queue
    while q:
      
        # Dequeue a vertex from queue and print it
        curr = q.popleft()
        print(curr, end=" ")

        # Get all adjacent vertices of the dequeued 
        # vertex. If an adjacent has not been visited, 
        # mark it visited and enqueue it
        for v in _graph.vertex_get_neighbors(curr): # ERRO AKI <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
			# Get the vertex index
            index = _graph.vertices.index(v)
            if not visited[index]:
                visited[index] = True
                q.append(v)
# ---------------------------- ----------------- --------------------------- #

# --------------------------------- Dijkstra ------------------------------- #

	# A utility function to find the vertex with
	# minimum distance value, from the set of vertices
	# not yet included in shortest path tree
def minDistance(dist, sptSet):

    # Initialize minimum distance for next node
    min = sys.maxsize

    # Search not nearest vertex not in the
    # shortest path tree
    for u in range(V):
        if dist[u] < min and sptSet[u] == False:
            min = dist[u]
            min_index = u

    return min_index

# Function that implements Dijkstra's single source
# shortest path algorithm for a graph represented
# using adjacency matrix representation
def dijkstra(source):

    dist = [sys.maxsize] * len(_graph.vertices)
    dist[source] = 0
    sptSet = [False] * len(_graph.vertices)

    for cout in range(len(_graph.vertices)):

        # Pick the minimum distance vertex from
        # the set of vertices not yet processed.
        # x is always equal to src in first iteration
        x = minDistance(dist, sptSet)

        # Put the minimum distance vertex in the
        # shortest path tree
        sptSet[x] = True

        # Update dist value of the adjacent vertices
        # of the picked vertex only if the current
        # distance is greater than new distance and
        # the vertex in not in the shortest path tree
        for y in range(len(_graph.vertices)): # ADAPTAR PRO CÓDIGO NOSSO <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            if self.graph[x][y] > 0 and sptSet[y] == False and \
                    dist[y] > dist[x] + self.graph[x][y]: 
                dist[y] = dist[x] + self.graph[x][y]

    printSolution(dist)

# Print the Dijkstra solution	 
def printSolution(self, dist): # ADAPTAR PRO CÓDIGO NOSSO <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        print("Vertex \tDistance from Source")
        for node in range(len(_graph.vertices)):
            print(node, "\t", dist[node])
# ---------------------------- ----------------- --------------------------- #

# ----------------------------------------------------------------------------- #
#                                   Main Loop                                   #
# ----------------------------------------------------------------------------- #

# Loop until menu told to quit.
while(True):
	if (menu()): 
		break
