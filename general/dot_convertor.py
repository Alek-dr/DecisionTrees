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

def export(graph,name):
    dot = 'digraph Tree { \n' \
          'node [shape=box, style="filled, rounded", color="black", fontname=helvetica] ; \n' \
          'edge [fontname=helvetica] ;\n'
    count = 0
    if isinstance(graph,DecisonTree):
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
    text_file = open(name + ".dot", "w")
    text_file.write(dot)
    text_file.close()