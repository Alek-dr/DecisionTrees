
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

class Node():
    def __init__(self,id):
        self.__id = id

    @property
    def id(self):
        return self.__id

class BinaryTree():

    def __init__(self):
        self.__left_node = None
        self.__right_node = None

    @property
    def left_node(self):
        return self.__left_node

    @property
    def right_node(self):
        return self.__left_node

    @left_node.setter
    def left_node(self, node):
        self.__left_node = node

    @right_node.setter
    def right_node(self, node):
        self.__right_node = node
