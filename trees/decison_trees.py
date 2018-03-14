from trees_algorithms.algorithms import *
from preprocess.convert import convert_categorial
from numpy import ravel

class DecisonTree():

    def __init__(self):
        self.tree = None
        self.categories = {}
        self.target = None
        self.states = {}
        self.name = "Decision tree"

    def learnID3(self,df,target_class,min_samples=4):

        self.target = target_class
        df, self.categories = convert_categorial(df)

        for col in df:
            if col in self.categories:
                s = len(df[col].unique())
                self.states[col] = s

        self.tree = Tree()
        self.tree.id3(df,self.target,self.categories,parent_id=0,states=self.states)

        # self.tree = DecisionBinaryTree()
        # self.tree.makeID3(df,self.target,self.categories,self.states,min_samples)
        # self.tree.reset_counter()
        #
        # self.__vertices, self.__edges = self.tree.get_vertices(v=self.tree)

    def print_tree(self):
        self.tree.print_tree()

    @property
    def vertices(self):
        return self.tree.vertices


    @property
    def edges(self):
        return self.tree.edges

    def get_node(self,id):
        return self.tree.get_node(id)

    def get_child(self,id):
        child = []
        for edg in self.edges:
            if edg[0]==id:
                child.append(edg[1:])
        child = ravel(child).tolist()
        return child



