from general.structures import *
from general.criterions import entropy, gini, D, D_continous, criterions
from general.help_functions import get_subdictionary
from numpy import abs, round, arange, average, log2

class DecisionBinaryTree(BinaryTree):

    def __init__(self):
        BinaryTree.__init__(self)
        self.node = Node(self.id)

    def makeID3(self,df,target,categories,states,min_samples,criterion="entropy"):

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
            initial_entropy = entropy(df, target, st)
            for col in df:
                if col != target:
                    if col in categories:
                        q = [i for i in range(states[col])]
                        h = 0
                        for i in q:
                            dq = df[df[col] == i]
                            num = dq.shape[0]
                            den = df.shape[0]
                            h += (num / den) * entropy(dq, target, st)
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
                            h += (num / den) * entropy(dq, target, st)

                            dq = df[df[col] > i]
                            num = dq.shape[0]
                            den = df.shape[0]
                            h += (num / den) * entropy(dq, target, st)

                            tresh_entr[i] = h
                        min_entr_key = min(tresh_entr, key=tresh_entr.get)
                        min_entr = tresh_entr[min_entr_key]
                        # Find keys with min entropy
                        keys = [k for k,v in tresh_entr.items() if v==min_entr]
                        col_tresh[col] = round(average(keys),3)
                        gain[col] = initial_entropy - tresh_entr[min_entr_key]
            # Find predicate
            beta = max(gain, key=gain.get)
            # If predicat cateogrial
            if beta in categories.keys():
                entropy_state = {}
                # For each possible state find entropy
                for i in range(states[beta]):
                    sub = df[df[beta]==i]
                    H = entropy(sub,target,[i])
                    entropy_state[i] = H
                # Get state with max entropy
                max_entropy = max(entropy_state, key=entropy_state.get)
                # Left node <state != max_entropy_state>
                # Right node <state == max_entropy_state>
                self.node.predicate = beta + " = " + str(max_entropy)
                self.node.categorical = True
                left_subs = df.loc[(df[beta] != max_entropy)]
                right_subs = df.loc[(df[beta] == max_entropy)]
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

class Tree(Graph):

    def __init__(self):
        Graph.__init__(self)

    def __id3__(self,df,target,categories,parent_id,states,criteria="enthropy", pred_value=None,parent_predicate=None):
        """
        Return graph what represents decision tree.

        Parameters
        ----------

        df: pandas dataframe.
            Train dataset
        target: string.
            Column of df. Target feature.
        categories: dictionary.
            contains corresponds between categorical and numeric values.
        parent_id: int.
            parent node id.
        states: dictionary.
             contains attributes and all possible states.
        pred_value: int.
            value of parent predicate, to get in this node.
        parent_predicate: string.
            parent node predicate.

        Returns
        -------
        decision tree
        """
        if criteria not in criterions:
            criteria = 'gini'

        if len(self.vertices)==0:
            node_id = 0
        else:
            node_id = len(self.vertices)

        if df.empty:
            node = Node(id=node_id,label='-')
            if pred_value!=None:
                node.pred_value = pred_value
            if parent_predicate!=None:
                node.parent_predicate = parent_predicate
            self.add_vertex(node)
            self.add_edge([parent_id,node_id])
            return

        unique = df[target].unique()
        if len(unique) == 1:
            node = Node(node_id,label=df[target][df.index.values[0]],samples=df.shape[0],categorial=True)
            if pred_value!=None:
                node.pred_value = pred_value
            if parent_predicate!=None:
                node.parent_predicate = parent_predicate
            self.add_vertex(node)
            self.add_edge([parent_id, node.id])
            return

        if len(categories)==0 or (len(categories)==1 and target in categories):
            numb = df[target].value_counts()
            prob = round(numb.max() / len(df), 2)
            node = Node(node_id,label=numb.idxmax(),samples=df.shape[0],prob=prob)
            if pred_value!=None:
                node.pred_value = pred_value
            if parent_predicate!=None:
                node.parent_predicate = parent_predicate
            self.add_vertex(node)
            self.add_edge([parent_id, node.id])
            return

        gain = {} # Gain actually can be gini index or gain ratio
        st = [i for i in range(states[target])]

        if criteria == 'entropy' or criteria == 'gain_ratio':
            initial_estimation = entropy(df, target, st)
        elif criteria == 'gini':
            initial_estimation = gini(df, target, st)

        for attribute in df:
            if attribute != target:
                q = [i for i in range(states[attribute])]
                h = 0
                if criteria == 'D':
                    h = D(df,attribute,target,q)
                    gain[attribute] = h
                else:
                    split_info = 0
                    for i in q:
                        dq = df[df[attribute] == i]
                        num = dq.shape[0]
                        den = df.shape[0]
                        p = num / den
                        if criteria == 'entropy' or criteria == 'gain_ratio':
                            h += p*entropy(dq,target,st)
                        elif criteria == 'gini':
                            h += p*gini(dq,target,st)
                        elif criteria == 'D':
                            h += p*D(dq,target,st)
                        if criteria == 'gain_ratio':
                            if p!=0:
                                # Do not try to get log2 of zero
                                split_info += -p*log2(p)
                    if criteria == 'gain_ratio':
                        gain[attribute] = (initial_estimation - h)/split_info
                    elif criteria == 'entropy' or criteria == 'gini':
                        gain[attribute] = initial_estimation - h

        # Find predicate
        beta = max(gain, key=gain.get)

        # Make the node
        node = Node(id=node_id, type='internal',predicate=beta,
                    samples=df.shape[0],categorial=True)
        node.criteria = round(gain[beta],4)

        if pred_value != None:
            node.pred_value = pred_value
        if parent_predicate != None:
            node.parent_predicate = parent_predicate

        # Add node to the graph
        self.add_vertex(node)
        if node_id!=0:
            self.add_edge([parent_id,node.id])

        # Making arcs
        sub_categories = get_subdictionary(categories,beta)
        # For each possible state get subset
        for i in range(states[beta]):
            sub_set = df[df[beta] == i].drop(beta,axis=1)
            self.__id3__(sub_set,target,sub_categories,node.id,states,criteria,i,beta)

    def __c45__(self,df,target,categories,parent_id,states,criteria="enthropy", pred_value=None,parent_predicate=None, isBigger=None):
        """
        Return graph what represents decision tree.

        Parameters
        ----------

        df: pandas dataframe.
            Train dataset
        target: string.
            Column of df. Target feature.
        categories: dictionary.
            contains corresponds between categorical and numeric values.
        parent_id: int.
            parent node id.
        states: dictionary.
             contains attributes and all possible states.
        pred_value: float.
            value of parent predicate to get into this node.
        parent_predicate: string.
            parent node predicate.
        isBigger: bool.
            if parent predicat is continous then is Bigger defines left or right subset.

        Returns
        -------
        decision tree
        """
        if criteria not in criterions:
            criteria = 'gini'

        if len(self.vertices)==0:
            node_id = 0
        else:
            node_id = len(self.vertices)

        if df.empty:
            node = Node(id=node_id,label='-')
            if pred_value!=None:
                node.pred_value = pred_value
            if parent_predicate!=None:
                node.parent_predicate = parent_predicate
            self.add_vertex(node)
            self.add_edge([parent_id,node_id])
            return

        unique = df[target].unique()
        if len(unique) == 1:
            if isBigger==None:
                categorial = True
            else:
                categorial = False
            node = Node(node_id,label=df[target][df.index.values[0]],samples=df.shape[0],categorial=categorial)
            if pred_value!=None and parent_predicate!=None:
                node.pred_value = pred_value
                if not categorial:
                    node.isBigger = isBigger
                node.parent_predicate = parent_predicate
            self.add_vertex(node)
            self.add_edge([parent_id, node.id])
            return

        if len(categories)==0 or (len(categories)==1 and target in categories and len(df.columns)==1):
            numb = df[target].value_counts()
            prob = round(numb.max() / len(df), 2)
            node = Node(node_id,label=numb.idxmax(),samples=df.shape[0],prob=prob)
            if pred_value!=None:
                node.pred_value = pred_value
            if parent_predicate!=None:
                node.parent_predicate = parent_predicate
            self.add_vertex(node)
            self.add_edge([parent_id, node.id])
            return

        col_tresh = {} # For continous attributes
        gain = {} # Gain actually can be gini index or gain ratio
        st = [i for i in range(states[target])]

        if criteria == 'entropy' or criteria == 'gain_ratio':
            initial_estimation = entropy(df, target, st)
        elif criteria == 'gini':
            initial_estimation = gini(df, target, st)

        for attribute in df:
            if attribute != target:
                if attribute in categories:
                    q = [i for i in range(states[attribute])]
                    h = 0
                    if criteria == 'D':
                        h = D(df,attribute,target,q)
                        gain[attribute] = h
                    else:
                        split_info = 0
                        for i in q:
                            dq = df[df[attribute] == i]
                            num = dq.shape[0]
                            den = df.shape[0]
                            p = num / den
                            if criteria == 'entropy' or criteria == 'gain_ratio':
                                h += p*entropy(dq,target,st)
                            elif criteria == 'gini':
                                h += p*gini(dq,target,st)
                            elif criteria == 'D':
                                h += p*D(dq,target,st)
                            if criteria == 'gain_ratio':
                                if p!=0:
                                    # Do not try to get log2 of zero
                                    split_info += -p*log2(p)
                        if criteria == 'gain_ratio':
                            gain[attribute] = (initial_estimation - h)/split_info
                        elif criteria == 'entropy' or criteria == 'gini':
                            gain[attribute] = initial_estimation - h
                else:
                    step = round((abs(df[attribute].max()) - abs(df[attribute].min())) / (df.shape[0]), 5)
                    if df[attribute].min() == df[attribute].max():
                        continue
                    q = list(arange(df[attribute].min(), df[attribute].max(), step).round(5))
                    tresh_entr = {}
                    split_info = 0
                    for i in q:
                        h = 0
                        if criteria == 'D':
                            h = D_continous(df, attribute, target, i)
                            tresh_entr[i] = h
                        else:
                            dq = df[df[attribute] <= i]
                            num = dq.shape[0]
                            den = df.shape[0]
                            if criteria == 'entropy' or criteria == 'gain_ratio':
                                h += (num / den) * entropy(dq, target, st)
                            elif criteria == 'gini':
                                h += (num / den) * gini(dq, target, st)
                            if criteria == 'gain_ratio':
                                if (num / den) != 0:
                                    split_info += -(num / den) * log2(num / den)

                            dq = df[df[attribute] > i]
                            num = dq.shape[0]
                            den = df.shape[0]
                            if criteria == 'entropy' or criteria == 'gain_ratio':
                                h += (num / den) * entropy(dq, target, st)
                            elif criteria == 'gini':
                                h += (num / den) * gini(dq, target, st)
                            if criteria == 'gain_ratio':
                                if (num / den) != 0:
                                    split_info += -(num / den) * log2(num / den)
                            tresh_entr[i] = h

                    if criteria == 'D':
                        max_d_key = max(tresh_entr, key=tresh_entr.get)
                        max_d = tresh_entr[max_d_key]
                        # Find keys with max D
                        keys = [k for k, v in tresh_entr.items() if v == max_d]
                        col_tresh[attribute] = round(average(keys), 3)
                        gain[attribute] = max_d
                    else:
                        min_entr_key = min(tresh_entr, key=tresh_entr.get)
                        min_entr = tresh_entr[min_entr_key]
                        # Find keys with min entropy
                        keys = [k for k, v in tresh_entr.items() if v == min_entr]
                        col_tresh[attribute] = round(average(keys), 3)
                        if criteria == 'gain_ratio':
                            gain[attribute] = (initial_estimation - tresh_entr[min_entr_key]) / split_info
                        elif criteria == 'entropy' or criteria == 'gini':
                            gain[attribute] = initial_estimation - tresh_entr[min_entr_key]

        # Find predicate
        beta = max(gain, key=gain.get)
        if beta in categories.keys():
            categorial = True
        else:
            categorial = False

        # Make the node
        node = Node(id=node_id, type='internal',predicate=beta,
                    samples=df.shape[0],categorial=categorial)
        node.criteria = round(gain[beta],4)


        if pred_value!=None:
            node.pred_value = str(pred_value)

        if parent_predicate != None:
            node.parent_predicate = parent_predicate

        # Add node to the graph
        self.add_vertex(node)
        if node_id!=0:
            self.add_edge([parent_id,node.id])

        # Making arcs
        sub_categories = get_subdictionary(categories,beta)

        # For each possible state get subset
        if beta in categories.keys():
            for i in range(states[beta]):
                sub_set = df[df[beta] == i].drop(beta,axis=1)
                self.__c45__(sub_set,target,sub_categories,node.id,states,criteria,i,beta)
        else:
            sub_set = df[(df[beta] <= col_tresh[beta])].drop(beta,axis=1)
            self.__c45__(sub_set, target, sub_categories, node.id, states, criteria, col_tresh[beta], beta, isBigger=False)
            sub_set = df[(df[beta] > col_tresh[beta])].drop(beta,axis=1)
            self.__c45__(sub_set, target, sub_categories, node.id, states, criteria, col_tresh[beta], beta, isBigger=True)

    def __predict__(self,sample,node,categories):
        """
        :param sample: Series sample to classify.
        :param node: current node.
        :param categories: dictionary from DecisionTrees.
        :return: class label.
        """
        if node.type!='leaf':
            p = node.predicate
            val = sample[p]
            child = self.get_child(node.id)
            for ch in child:
                node = self.get_node(ch)
                if node.isBigger == None:
                    categorial = True
                else:
                    categorial = False
                if categorial:
                    if float(node.pred_value)==float(val):
                        return self.__predict__(sample,node,categories)
                else:
                    if node.isBigger==False:
                        if float(val) <= float(node.pred_value):
                            return self.__predict__(sample, node, categories)
                    else:
                        if float(val) > float(node.pred_value):
                            return self.__predict__(sample, node, categories)

        else:
            return node.label



