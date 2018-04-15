from trees.decison_trees import *
from general.help_functions import get_category

def add_node_label(node,categories,target,criteria,write_index=False,write_samles=False,write_criteria=True):
    label = ""
    if write_index==True:
        label += "Id = {}\n".format(node.id)
    if node.parent_predicate!=None:
        if node.parent_predicate in categories.keys():
            states = categories[node.parent_predicate]
            for k,v in states.items():
                if v==node.pred_value:
                    label += "{} = {}\n".format(node.parent_predicate,k)
                    break
        else:
            label += "{}\n".format(node.pred_value)
    if node.type=='internal':
        if node.predicate!=None:
            label += "Predicate = {}\n".format(node.predicate)
    if write_criteria == True:
        if node.criteria!=None:
            if criteria=='entropy':
                label += "Information gain = {}\n".format(node.criteria)
            elif criteria=='gain_ratio':
                label += "Gain ratio = {}\n".format(node.criteria)
            elif criteria=='gini':
                label += "Gini = {}\n".format(node.criteria)
            elif criteria=='D':
                label += "D = {}\n".format(node.criteria)
    if write_samles==True:
        if node.samples!=None:
            label+="Samples = {}\n".format(node.samples)
    if node.type=="leaf":
        if node.probability!=None:
            label += "Prob = {}\n".format(node.probability)
        if node.label!=None:
            if node.label=='-':
                label_name = '-'
            else:
                label_name = get_category(categories, target, node.label)
            label += "Class = {}".format(label_name)
    return "[label=\"{}\", fillcolor=\"{}\"];\n".format(label,"#ffffff")

def export(graph,name):
    dot = 'digraph Tree { \n' \
          'node [shape=box, style="filled, rounded", color="black", fontname=helvetica] ; \n' \
          'edge [fontname=helvetica] ;\n'

    if isinstance(graph.tree,Tree):
        for v in graph.vertices:
            dot += str(v.id) + add_node_label(v,graph.categories,graph.target,graph.criteria,
                                              write_index=True,write_samles=True,write_criteria=True)
            child = graph.get_child(v.id)
            for ch in child:
                child_node = graph.get_node(ch)
                dot += str(child_node.id) +  add_node_label(child_node,graph.categories,graph.target, graph.criteria,
                                                            write_index=True,write_samles=True, write_criteria=True)
                dot += "{} -> {};\n".format(v.id, child_node.id)
        dot += '}'

    text_file = open(name + ".dot", "w")
    text_file.write(dot)
    text_file.close()