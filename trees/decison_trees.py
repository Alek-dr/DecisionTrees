from general.structures import DecisionBinaryTree
from preprocess.convert import convert_categorial

class DecisonTree():

    def __init__(self):
        self.tree = None
        self.categories = {}
        self.target = None
        self.states = {}
        self.name = "Decision tree"
        self.__vertices = 0
        self.__edges = []

    def learnID3(self,df,target_class):

        self.target = target_class
        df, self.categories = convert_categorial(df)

        for col in df:
            if col in self.categories:
                s = len(df[col].unique())
                self.states[col] = s

        self.tree = DecisionBinaryTree()
        self.tree.makeID3(df,self.target,self.categories,self.states)
        self.tree.reset_counter()

        self.__vertices, self.__edges = self.tree.get_vertices(v=self.tree)

    def print_tree(self):
        self.tree.print_tree()

    @property
    def vertices(self):
        return self.__vertices

    @property
    def edges(self):
        return self.__edges

    @vertices.setter
    def vertices(self, num_vertices):
        if num_vertices > 0:
            self.__vertices = num_vertices
        else:
            raise Exception("Vertices numbers must be above zero")

    def add_edge(self, edge):
        if isinstance(edge, list) and (len(edge) == 2):
            self.__edges.append(edge)

    def delete_edge(self, edge):
        if edge in self.__edges:
            self.__edges.remove(edge)
        else:
            raise Exception("Edge not in graph")



