from numpy import ravel

class Graph():

    def __init__(self):
        self.__vertices = []
        self.__edges = []
        self.__node = None

    @property
    def vertices(self):
        return self.__vertices

    @property
    def edges(self):
        return self.__edges

    def add_vertex(self,v):
        self.__vertices.append(v)

    def add_edge(self, edge):
        if isinstance(edge, list) and (len(edge)==2):
            self.__edges.append(edge)

    def delete_edge(self,edge):
        if edge in self.__edges:
            self.__edges.remove(edge)
        else:
            raise Exception("Edge not in graph")

    def get_node(self,id):
        for node in self.vertices:
            if node.id == id:
                return node

    def get_child(self,id):
        """
        :param id:
        :return: list of child ids
        """
        child = []
        for edg in self.__edges:
            if edg[0]==id:
                child.append(edg[1:])
        child = ravel(child).tolist()
        return child

    def get_parent(self,id):
        for edg in self.edges:
            if edg[1]==id:
                return edg[0]
        return -1

    def get_rel_depth(self,id):
        depth = 1
        parent = self.get_parent(id)
        while parent!=-1:
            depth+=1
            parent = self.get_parent(parent)
        return depth

    def get_depth(self):
        if len(self.vertices)==0:
            return 0
        vertices = [self.vertices[0]]
        max_depth = 1
        for v in vertices:
            ch_id = self.get_child(v.id)
            vertices.pop()
            if len(ch_id)>0:
                max_depth+=1
            for ch in ch_id:
                vertices.append(self.get_node(ch))
        return max_depth

class Node():

    def __init__(self,id,type='leaf',label=None,predicate=None,samples=0,categorial=False,prob=None, isBigger=None):
        self.__id = id
        self.__type = type
        self.__y = label
        self.__predicate = predicate
        self.__samples = samples
        self.__categorical = categorial
        self.__prob = prob
        self.__isBigger = isBigger
        self.__predicate_value = None
        self.__parent_predicate = None
        self.__criteria_value = None

    @property
    def isBigger(self):
        return self.__isBigger

    @isBigger.setter
    def isBigger(self,v):
        if isinstance(v,bool):
            self.__isBigger = v
        else:
            pass

    @property
    def criteria(self):
        return self.__criteria_value

    @criteria.setter
    def criteria(self,v):
        self.__criteria_value = v

    @property
    def parent_predicate(self):
        return self.__parent_predicate

    @parent_predicate.setter
    def parent_predicate(self,v):
        self.__parent_predicate = v

    @property
    def pred_value(self):
        return self.__predicate_value

    @pred_value.setter
    def pred_value(self,v):
        self.__predicate_value = v

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
