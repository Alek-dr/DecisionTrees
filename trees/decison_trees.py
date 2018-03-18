from trees_algorithms.algorithms import *
from preprocess.convert import convert_categorial
from numpy import ravel
from general.criterions import criterions
from general.help_functions import *
from pandas import DataFrame,Series

class DecisonTree():

    def __init__(self):
        self.tree = None
        self.categories = {}
        self.target = None
        self.states = {}
        self.name = "Decision tree"
        self.criteria = None
        self.columns = []

    def learnID3(self,df,target_class,criteria="entropy",as_categories=[]):

        self.target = target_class

        if criteria not in criterions:
            self.criteria = 'gini'
        else:
            self.criteria = criteria
        self.columns = df.columns
        df, self.categories = convert_categorial(df,as_categories)

        for col in df:
            if col in self.categories:
                s = len(df[col].unique())
                self.states[col] = s

        self.tree = Tree()
        self.tree.__id3__(df,self.target,self.categories,parent_id=0,states=self.states,criteria=criteria)

    def predict(self,sample):
        label = ''
        if isinstance(sample,Series):
            sample = convert(sample,self.categories,self.columns)
            if isinstance(self.tree,Tree):
                root = self.tree.get_node(0)
                label = self.tree.__predict__(sample,root,self.categories)
                label = get_category(self.categories, self.target, label)
        return label

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



