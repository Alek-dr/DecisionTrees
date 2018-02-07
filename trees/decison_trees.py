from general.structures import DecisionBinaryTree
from general.criterions import enthropy
from preprocess.convert import convert_categorial

class DecisonTree():

    def __init__(self):
        self.tree = None
        self.categories = {}
        self.target = None
        self.states = {}
        self.name = "Decision tree"

    def learnID3(self,df,target_class):

        self.target = target_class
        df, self.categories = convert_categorial(df)

        for col in df:
            s = len(df[col].unique())
            self.states[col] = s

        self.tree = DecisionBinaryTree()
        self.tree._id = 0
        self.tree.makeID3(df,self.target,self.categories,self.states)
        #self.tree.dfs(self.tree)

    def print_tree(self):
        self.tree.print_tree()



