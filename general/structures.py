from general.criterions import enthropy
from numpy import abs, round, arange, average

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

    __count__ = 0

    def __init__(self):
        self.__left_node = None
        self.__right_node = None
        self.__id = BinaryTree.__count__
        BinaryTree.__count__ += 1

    @property
    def id(self):
        return self.__id

    def reset_counter(self):
        BinaryTree.__count__ = 0

    @property
    def left_node(self):
        return self.__left_node

    @property
    def right_node(self):
        return self.__right_node

    @left_node.setter
    def left_node(self, node):
        self.__left_node = node

    @right_node.setter
    def right_node(self, node):
        self.__right_node = node

class DecisionBinaryTree(BinaryTree):

    def __init__(self):
        BinaryTree.__init__(self)
        self._type = "leaf"
        self._y = 0
        self._predicate = None
        self._samples = 0

    @property
    def type(self):
        return self._type

    def makeID3(self,df,target,categories,states):

        unique = df[target].unique()

        if len(unique) == 1:
            self._y = df[target][df.index.values[0]]
            self._samples = df.shape[0]
        else:
            self._type = "internal"
            gain = {}
            col_tresh = {}
            st = [i for i in range(states[target])]
            initial_entropy = enthropy(df, target, st)
            for col in df:
                if col != target:
                    if col in categories:
                        q = [i for i in range(states[col])]
                        h = 0
                        for i in q:
                            dq = df[df[col] == i]
                            num = dq.shape[0]
                            den = df.shape[0]
                            h += (num / den) * enthropy(dq, target, st)
                        gain[col] = initial_entropy - h
                    else:
                        step = round((abs(df[col].min())+abs(df[col].max()))/(df[col].shape[0]),5)
                        q = list(arange(df[col].min(),df[col].max(),step).round(5))
                        if df[col].min()==df[col].max():
                            continue
                        tresh_entr = {}
                        for i in q:
                            h = 0

                            dq = df[df[col] <= i]
                            num = dq.shape[0]
                            den = df.shape[0]
                            h += (num / den) * enthropy(dq, target, st)

                            dq = df[df[col] > i]
                            num = dq.shape[0]
                            den = df.shape[0]
                            h += (num / den) * enthropy(dq, target, st)

                            tresh_entr[i] = h
                        min_entr_key = min(tresh_entr, key=tresh_entr.get)
                        min_entr = tresh_entr[min_entr_key]
                        # Find keys with min entr
                        keys = [k for k,v in tresh_entr.items() if v==min_entr]
                        col_tresh[col] = round(average(keys),3)
                        gain[col] = initial_entropy - tresh_entr[min_entr_key]
            # Find predicate
            beta = max(gain, key=gain.get)
            # If predicat cateogrial
            if beta in categories.keys():
                enthropy_state = {}
                # For each possible state find enthropy
                for i in range(states[beta]):
                    sub = df[df[beta]==i]
                    H = enthropy(sub,target,[i])
                    enthropy_state[i] = H
                # Get state with max enthropy
                max_enthropy = max(enthropy_state, key=enthropy_state.get)
                # Left node <state != max_enthropy_state>
                # Right node <state == max_enthropy_state>
                self._predicate = beta + " = " + str(max_enthropy)
                left_subs = df.loc[(df[beta] != max_enthropy)]
                right_subs = df.loc[(df[beta] == max_enthropy)]
                prob = {}
                if left_subs.empty:
                    m = right_subs.shape[0]
                    for i in range(states[target]):
                        prob[i] = df[df[target] == i].shape[0] / m
                if right_subs.empty:
                    m = left_subs.shape[0]
                    for i in range(states[target]):
                        prob[i] = df[df[target] == i].shape[0] / m
                # If node is leaf
                if len(prob)>0:
                    self._predicate = None
                    self._type = "leaf"
                    self._y = max(prob, key=prob.get)
                else:
                    self.left_node = DecisionBinaryTree()
                    self.right_node = DecisionBinaryTree()
                    self.left_node.makeID3(left_subs,target,categories,states)
                    self.right_node.makeID3(right_subs,target,categories,states)
            else:
                self._predicate = beta + " <= " + str(col_tresh[beta])
                left_subs = df.loc[(df[beta] <= col_tresh[beta])]
                right_subs = df.loc[(df[beta] > col_tresh[beta])]
                prob = {}
                if left_subs.empty:
                    m = right_subs.shape[0]
                    for i in range(states[target]):
                        prob[i] = df[df[target] == i].shape[0] / m
                if right_subs.empty:
                    m = left_subs.shape[0]
                    for i in range(states[target]):
                        prob[i] = df[df[target] == i].shape[0] / m
                # If node is leaf
                if len(prob)>0:
                    self._predicate = None
                    self._type = "leaf"
                    self._y = max(prob, key=prob.get)
                else:
                    self.left_node = DecisionBinaryTree()
                    self.right_node = DecisionBinaryTree()
                    self.left_node.makeID3(left_subs,target,categories,states)
                    self.right_node.makeID3(right_subs,target,categories,states)


    def print_tree(self):
        pass