from trees_algorithms.algorithms import *
from preprocess.convert import convert_categorial
from numpy import ravel
from general.criterions import criterions
from general.help_functions import *
from pandas import Series

class DecisonTree():

    def __init__(self):
        self.tree = None
        self.name = "Decision tree"
        self.columns = []

    def learnID3(self,df,target_class,params):

        criteria = params['criteria']
        if 'as_categories' in params:
            as_categories = params['as_categories']
        else:
            as_categories = []

        self.columns = df.columns
        df, categories = convert_categorial(df, as_categories)

        states = {}
        for col in df:
            if col in categories:
                s = len(df[col].unique())
                states[col] = s

        self.tree = Tree()
        self.tree.target = target_class
        if criteria in criterions:
            self.tree.criteria = criteria
        self.tree.categories = categories
        self.tree.states = states
        self.tree.__id3__(df, parent_id=0)

    def learnC45(self,df,target_class,params):

        criteria = params['criteria']
        if 'as_categories' in params:
            as_categories = params['as_categories']
        else:
            as_categories = []

        self.columns = df.columns
        df, categories = convert_categorial(df,as_categories)

        states = {}
        for col in df:
            if col in categories:
                s = len(df[col].unique())
                states[col] = s

        self.tree = Tree()
        self.tree.target = target_class
        if 'max_depth' in params:
            self.tree.max_depth = params['max_depth']
        if 'min_samples' in params:
            self.tree.min_samples = params['min_samples']
        if criteria in criterions:
            self.tree.criteria = criteria
        self.tree.categories = categories
        self.tree.states = states
        self.tree.__c45__(df, parent_id=0)
        if ('postprune' in params) and (params['postprune'] == True):
            self.tree.postpruing(df)

    def predict(self,sample):
        label = ''
        if isinstance(sample,Series):
            sample = convert(sample,self.categories)
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



