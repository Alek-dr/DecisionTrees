import pandas as pd
from trees.decison_trees import DecisonTree
from general import dot_convertor

#data_set = pd.read_csv('datasets/zenit.csv')
#data_set = pd.read_csv('datasets/Iris.csv')
data_set = pd.read_csv('datasets/PlayTennis.csv')

tree = DecisonTree()

#data_set.drop("Id",axis=1,inplace=True)
#data_set.drop("Day",axis=1,inplace=True)

tree.learnID3(data_set,'Play', as_categories=["Day"], criteria='gain_ratio')

#dot_convertor.export(tree,"PlayTennis_gr")