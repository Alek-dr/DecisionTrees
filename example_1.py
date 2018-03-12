import pandas as pd
from trees.decison_trees import DecisonTree
from general import dot_convertor

#data_set = pd.read_csv('datasets/zenit.csv')
data_set = pd.read_csv('datasets/Iris.csv')

tree = DecisonTree()

data_set.drop("Id",axis=1,inplace=True)

tree.learnID3(data_set,'Species',min_samples=3)

dot_convertor.export(tree,"my_iris")