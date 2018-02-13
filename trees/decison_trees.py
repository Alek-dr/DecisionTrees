from general.structures import DecisionBinaryTree
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
            if col in self.categories:
                s = len(df[col].unique())
                self.states[col] = s

        self.tree = DecisionBinaryTree()
        self.tree.makeID3(df,self.target,self.categories,self.states)
        self.tree.reset_counter()

    def print_tree(self):
        self.tree.print_tree()



