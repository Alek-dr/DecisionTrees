from general.structures import BinaryTree
from general.criterions import enthropy
from preprocess.convert import convert_categorial
import operator

class DecisonBinaryTree(BinaryTree):

    categories = {}
    states = {}
    target = None

    def __init__(self):
        self._type = "leaf"
        self._y = 0
        self._predicate = None

    @property
    def type(self):
        return self._type

    def makeID3(self,df):

        unique = df[self.target].unique()

        if len(unique)==1:
            tree = DecisonBinaryTree()
            tree._y = df[self.target][df.index.values[0]]
            return tree
        else:
            gain = {}
            initial_entropy = enthropy(df,self.target,self.states[self.target])
            for col in df:
                if col!=self.target:
                    if col in self.categories:
                        q = self.states[col]
                        h = 0
                        for i in range(q):
                            dq = df[df[col]==i]
                            num = dq.shape[0]
                            den = df.shape[0]
                            h += (num/den)*enthropy(dq,self.target,q)
                        gain[col] = initial_entropy - h
                    else:
                        pass
            #Find predicate
            beta = max(gain, key=gain.get)
            self._predicate = beta
            if beta in self.categories.keys():
                left_subs = df.loc[(df[beta] == i)]
                right_subs = df.loc[(df[beta] != i)]
                self._left_node = DecisonBinaryTree()
                self._left_node.makeID3(left_subs)
                self._right_node = DecisonBinaryTree().makeID3(right_subs)
            else:
                pass

    def learnID3(self,df,target_class):

        self.target = target_class
        df, self.categories = convert_categorial(df)

        for col in df:
            s = len(df[col].unique())
            self.states[col] = s

        self.makeID3(df)

    def print_tree(self):
        if self._predicate!=None:
            print(self._predicate)
        # if self._left_node!=None:
        #     self._left_node.print_tree()
        # if self._right_node != None:
        #     self._right_node.print_tree()



