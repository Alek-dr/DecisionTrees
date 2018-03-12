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
        self.__type = "leaf"
        self.__y = None
        self.__predicate = None
        self.__samples = 0
        self.__categorical = False
        self.__prob = None

    @property
    def id(self):
        return self.__id

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self,t):
        self.__type = t

    @property
    def label(self):
        return self.__y

    @label.setter
    def label(self,l):
        self.__y = l

    @property
    def predicate(self):
        return self.__predicate

    @predicate.setter
    def predicate(self,p):
        self.__predicate = p

    @property
    def samples(self):
        return self.__samples

    @samples.setter
    def samples(self,n):
        self.__samples = n

    @property
    def categorical(self):
        return self.__categorical

    @categorical.setter
    def categorical(self,v):
        self.__categorical = v

    @property
    def probability(self):
        return self.__prob

    @probability.setter
    def probability(self,v):
        self.__prob = v

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
        self.node = Node(self.id)

    def makeID3(self,df,target,categories,states,min_samples):

        unique = df[target].unique()

        if len(unique) == 1:
            self.node.label = df[target][df.index.values[0]]
            self.node.samples = df.shape[0]
        else:
            self.node.type = "internal"
            self.node.samples = df.shape[0]
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
                self.node.predicate = beta + " = " + str(max_enthropy)
                self.node.categorical = True
                left_subs = df.loc[(df[beta] != max_enthropy)]
                right_subs = df.loc[(df[beta] == max_enthropy)]
            else:
                self.node.predicate = beta + " <= " + str(col_tresh[beta])
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
                self.node.predicate = None
                self.node.type = "leaf"
                self.node.label = max(prob, key=prob.get)
            elif len(left_subs) <= min_samples or len(right_subs) <= min_samples:
                numb = df[target].value_counts()
                self.node.predicate = None
                self.node.type = "leaf"
                self.node.label = numb.idxmax()
                self.node.samples = df.shape[0]
                self.node.probability = round(numb.max() / len(df), 2)
            else:
                self.left_node = DecisionBinaryTree()
                self.right_node = DecisionBinaryTree()
                self.left_node.makeID3(left_subs,target,categories,states,min_samples)
                self.right_node.makeID3(right_subs,target,categories,states,min_samples)

    def get_vertices(self,v,vertices=[],edges=[]):
        if v.node.id not in vertices:
            vertices.append(v.node.id)
            if v.node.type!="leaf":
                edges.append([v.node.id, v.left_node.id])
                edges.append([v.node.id,v.right_node.id])
                self.get_vertices(v.left_node,vertices,edges)
                self.get_vertices(v.right_node,vertices,edges)
        return vertices,edges

    def get_node(self,v,id):
        if v.node.id==id:
            return v.node
        else:
            if v.left_node is not None:
                node = self.get_node(v.left_node,id)
                if node:
                    return node
            if v.right_node is not None:
                node = self.get_node(v.right_node,id)
                if node:
                    return node