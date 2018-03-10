from general.structures import DecisionBinaryTree
from preprocess.convert import convert_categorial
from numpy import ravel

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

    def get_node(self,id):
        return self.tree.get_node(self.tree,id)

    def get_child(self,id):
        child = []
        for edg in self.edges:
            if edg[0]==id:
                child.append(edg[1:])
        child = ravel(child).tolist()
        return child



