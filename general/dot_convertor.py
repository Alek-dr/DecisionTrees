from trees.decison_trees import *

def get_category(categories,key,val):
    for k,v in categories[key].items():
        if v==int(val):
            return k

def add_label(node,categories,target):
    label = ""
    if node.predicate!=None:
        if node.categorical:
            predicate = [s.strip() for s in node.predicate.split("=")]
            name = get_category(categories,predicate[0],predicate[1])
            label += predicate[0] + " = " + name
            del predicate
        else:
            label += node.predicate + '\n'
    if node.label!=None:
        class_name = get_category(categories, target, node.label)
        label += class_name + '\n'
    if node.samples != None:
        label += "Samples = " + str(node.samples) + '\n'
    if node.probability != None:
        label += "Probability = " + str(node.probability)
    return str(node.id) + "[label=\"{}\", fillcolor=\"{}\"];\n".format(label,"#ffffff")

def add_node_label(node,categories,target,write_index=False,write_samles=False):
    label = ''
    if node.id==0:
        label += node.predicate
    else:
        if node.parent_predicate!=None:
            states = categories[node.parent_predicate]
            for k,v in states.items():
                if v==node.pred_value:
                    label += "{} = {}".format(node.parent_predicate,k)
                    if node.type == "internal":
                        label += '\n'
                    break
        if node.predicate!=None:
            label+="Predicate = {}".format(node.predicate)
        if write_samles == True:
            label += "\nSamples = {}".format(node.samples)
        if write_index == True:
            label += "\nId = {}\n".format(node.id)
    if node.type=='leaf':
        if node.label!=None:
            label_name = get_category(categories,target,node.label)
            label += "{}".format(label_name)

    return "[label=\"{}\", fillcolor=\"{}\"];\n".format(label,"#ffffff")

def export(graph,name):
    dot = 'digraph Tree { \n' \
          'node [shape=box, style="filled, rounded", color="black", fontname=helvetica] ; \n' \
          'edge [fontname=helvetica] ;\n'

    if isinstance(graph,DecisonTree):
        if isinstance(graph.tree,BinaryTree):
            count = 0
            for v in graph.vertices:
                node = graph.get_node(v)
                dot += add_label(node,graph.categories,graph.target)
                child = graph.get_child(v)
                for ch in child:
                    child_node = graph.get_node(ch)
                    dot += add_label(node,graph.categories,graph.target)
                    if count==0:
                        dot += "{} -> {} {} \n".format(node.id, child_node.id, '[labeldistance=2.5, labelangle=45, headlabel="True"]')
                        count+=1
                    elif count==1:
                        dot += "{} -> {} {} \n".format(node.id, child_node.id,
                                                       '[labeldistance=2.5, labelangle=-45, headlabel="False"]')
                        count += 1
                    else:
                        dot += "{} -> {}\n".format(node.id, child_node.id)
            dot += '}'

        elif isinstance(graph.tree,Tree):
            for v in graph.vertices:
                dot += str(v.id) + add_node_label(v,graph.categories,graph.target,write_index=True,write_samles=True)
                child = graph.get_child(v.id)
                for ch in child:
                    child_node = graph.get_node(ch)
                    dot += str(child_node.id) +  add_node_label(child_node,graph.categories,graph.target,write_index=True,write_samles=True)
                    dot += "{} -> {};\n".format(v.id, child_node.id)
            dot += '}'

    text_file = open(name + ".dot", "w")
    text_file.write(dot)
    text_file.close()