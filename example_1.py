from general.structures import BinaryTree, Node
import pandas as pd
from trees.decison_trees import DecisonBinaryTree
from preprocess.convert import convert_categorial
import os


data_set = pd.read_csv('datasets/zenit.csv')

#data_set, fcc = convert_categorial(data_set)

tree = DecisonBinaryTree()

#w = data_set['win'][0]


tree.learnID3(data_set,'win')

tree.print_tree()

#print(tree.categories)





