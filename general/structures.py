from general.criterions import enthropy

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

    def __init__(self):
        self.__left_node = None
        self.__right_node = None

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
            st = [i for i in range(states[target])]
            initial_entropy = enthropy(df, target, st)
            for col in df:
                if col != target:
                    if col in categories:
                        q = [i for i in range(states[col])]
                        #q = states[col]
                        h = 0
                        for i in q:
                            dq = df[df[col] == i]
                            num = dq.shape[0]
                            den = df.shape[0]
                            h += (num / den) * enthropy(dq, target, q)
                        gain[col] = initial_entropy - h
                    else:
                        pass
            # Find predicate
            beta = max(gain, key=gain.get)
            self._predicate = beta
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
                # Left node <state=max_enthropy_state>
                # Right node <state != max_enthropy_state>
                left_subs = df.loc[(df[beta] != max_enthropy)]
                right_subs = df.loc[(df[beta] == max_enthropy)]
                print(left_subs)
                print(right_subs)
                prob = {}
                if left_subs.empty:
                    m = right_subs.shape[0]
                    for i in range(states[target]):
                        prob[i] = df[df[target]==i].shape[0] / m
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
                pass

    def print_tree(self):
        pass