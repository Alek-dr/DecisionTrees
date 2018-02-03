
class Graph():

    def __init__(self):
        self.__vertices = 0
        self.__edges = []

    @property
    def vertices(self):
        return self.__vertices

    @property
    def edges(self):
        return self.__edges

    @vertices.setter
    def vertices(self, num_vertices):
        if num_vertices>0:
            self.__vertices = num_vertices
        else:
            raise Exception("Vertices numbers must be above zero")

    def add_edge(self, edge):
        if isinstance(edge, list) and (len(edge)==2):
            self.__edges.append(edge)

    def delete_edge(self,edge):
        if edge in self.__edges:
            self.__edges.remove(edge)
        else:
            raise Exception("Edge not in graph")
