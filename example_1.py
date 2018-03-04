import pandas as pd
from trees.decison_trees import DecisonTree

data_set = pd.read_csv('datasets/zenit.csv')

tree = DecisonTree()

#data_set.drop("Id",axis=1,inplace=True)

tree.learnID3(data_set,'win')

print(tree)
