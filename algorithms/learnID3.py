from general.structures import BinaryTree
from general.criterions import enthropy
from preprocess.convert import categorial2code
import operator

class DecisonBinaryTree(BinaryTree):

    def __init__(self):
        self.__type = "leaf"
        self.__y = 0

    @property
    def type(self):
        return self.__type


def make(tree,df,target,states):

    unique = df[target].unique()

    if len(unique)==1:
        tree.__y = df[target][0]
        return tree
    else:
        gain = {}
        initial_entropy = enthropy(df,target,states[target])
        for col in df:
            if col!=target:
                q = states[col]
                h = 0
                for i in range(q):
                    dq = df[df[col]==i]
                    num = dq.shape[0]
                    den = df.shape[0]
                    h += (num/den)*enthropy(dq,target,q)
                gain[col] = initial_entropy - h
        #Find predicate
        beta = max(gain, key=gain.get)
        target_counts = {}
        ind = []
        for i in reversed(range(states[beta])):
            subs = df.loc[(df[beta] >= i)]
            print(subs)
            target_counts[i] = df[df[beta] >= i].shape[0]
        U0 = df[df[beta]]


def fit(df,target_class):

    tree = DecisonBinaryTree()
    states = {}

    for col in df:
        s = len(df[col].unique())
        states[col] = s

    make(tree,df,target_class,states)



