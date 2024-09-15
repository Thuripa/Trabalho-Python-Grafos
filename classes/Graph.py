# ---------------------------------------------------------------------------- #
#                                    Vertex                                    #
# ---------------------------------------------------------------------------- #
class Vertex:
    def __init__(self, label, edges):
        self.label = label
        self.edges = edges # Useless?

# ---------------------------------------------------------------------------- #
#                                     Edge                                     #
# ---------------------------------------------------------------------------- #

class Edge:
    def __init__(self, origin, destination, weight):
        self.origin = origin
        self.destination = destination
        self.weight = weight

# ---------------------------------------------------------------------------- #
#                                  Graph Class                                 #
# ---------------------------------------------------------------------------- #

class Graph:
    # Constructor
    def __init__(self, weighted, directional):
        self.vertices = []
        self.edges = []
        self.weighted = weighted
        self.directional = directional

    # Returns a vertex by it's label, None if not found.
    def vertex_get(self, label):
        for v in self.vertices:
            if v.label == label:
                return v
        return None
    
    # Returns true if a vertex exists.
    def vertex_exists(self, label : str):
        return (self.vertex_get(label) != None)

    # Adds a empty vertex, not connected to anything yet.
    def vertex_add(self, label):
        if (self.vertex_exists(label)):
            return False
        self.vertices.append(Vertex(label, []))
        return True
    
    # Removes a vertex by a given label. Returns true if removed, or false if it doesn't exist.
    def vertex_remove(self, label : str):
        _vertex = self.vertex_get(label)
        if (_vertex == None):
            return False
        
        self.vertices.remove(_vertex)
        return True

    # Renames a vertex, by it's label. Returns true if renaming was made.
    def vertex_label(self, label : str, new_label : str):
        _vertex = self.vertex_get(label)
        _target = self.vertex_get(new_label)
        # Something failed while parsing the label we want to rename
        if (_vertex == None):
            return False
        # There already exists a label with the name we're trying to rename this one to.
        if (_target != None):
            return False
        
        # Rename the label safely.
        _vertex.label = new_label
        return True

    # Gets an edge given origin and destination. Returns None if not found.
    def edge_get(self, origin : str, destination : str):
        _origin = self.vertex_get(origin)
        _dest = self.vertex_get(destination)

        if (_origin == None or _dest == None):
            return None
        
        for e in self.edges:
            if (e.origin == _origin and e.destination == _dest):
                return e

        return None

    # Returns True if a edge exists given the parameters, False otherwise.
    def edge_exists(self, origin : str, destination : str):
        return (self.edge_get(origin, destination) != None)

    # Adds an edge. Returns true if edge was successfully added.
    def edge_add(self, origin, destination, weight = 0):
        _origin = self.vertex_get(origin)
        _dest = self.vertex_get(destination)
        
        if (_origin == None or _dest == None):
            return False

        self.edges.append(Edge(_origin, _dest, weight))
        return True
    
    # Removes an edge given a origin and destionation. Returns true if succeeded.
    def edge_remove(self, origin : str, destination : str):
        _edge = self.edge_get(origin, destination)
        if (_edge == None):
            return False

        # Remove from list.
        self.edges.remove(_edge)
        return True

    # Returns the weight of a given edge
    def edge_get_weight(self, origin : str, destination : str):
        _edge = self.edge_get(origin, destination)
        if (_edge == None):
            return 0 # ? Return something else?
        return _edge.weight

    # Returns the neighbors of the given vertex.
    def vertex_get_neighbors(self, label : str):
        _vertex = self.vertex_get(label)
        if (_vertex == None):
            return None

        _neighbors = []
        for e in self.edges:
            if (e.origin == _vertex):
                if not (e.destination in _neighbors):
                    _neighbors.append(e.destination)
            if (e.destination == _vertex):
                if not (e.origin in _neighbors):
                    _neighbors.append(e.origin)
        
        return _neighbors

    # Returns the adjacent vertices of the given vertex with respect to edge direction.
    def vertex_get_adjacent(self, label : str):
        _vertex = self.vertex_get(label)
        if (_vertex == None):
            return None

        _neighbors = []
        for e in self.edges:
            if (e.origin == _vertex):
                if not (e.destination in _neighbors):
                    _neighbors.append(e.destination)
            if (not self.directional) and (e.destination == _vertex):
                if not (e.origin in _neighbors):
                    _neighbors.append(e.origin)
        
        return _neighbors

    # Returns a list of all the vertex's edges.
    def vertex_get_edges(self, label : str):
        _vertex = self.vertex_get(label)
        if (_vertex == None):
            return None

        _edges = []
        for e in self.edges:
            if (e.origin == _vertex):
                if not (e in _edges):
                    _edges.append(e)
            if (not self.directional) and (e.destination == _vertex):
                if not (e in _edges):
                    _edges.append(e)
        
        return _edges

    # Returns a string listing all vertices that exist.
    def get_string_vertices(self):
        _s = "Vertices: ["
        for i in range(0, len(self.vertices)):
            _last = (i == len(self.vertices)-1)
            _v = self.vertices[i]
            _s += _v.label
            if not _last:
                _s += ", "
        _s += "]."
        return _s

    # Returns a string listing all edges that exist.
    def get_string_edges(self):
        _s = "Edges: ["
        for i in range(0, len(self.edges)):
            _last = (i == len(self.edges)-1)
            _e = self.edges[i]
            _s += f"({_e.origin.label}, {_e.destination.label})"
            if not _last:
                _s += ", "
        _s += "]."
        return _s