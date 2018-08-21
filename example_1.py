import pandas as pd
from trees.decison_trees import DecisonTree
from general import dot_convertor

data_set = pd.read_csv('datasets/zenit.csv')

tree = DecisonTree()

data_set.drop("day",axis=1,inplace=True)
sample = data_set.copy()

params = {'criteria':'entropy','postprune':True}
tree.learnC45(data_set,'win',params)

predict = []
for i,row in sample.iterrows():
    label = tree.predict(row)
    predict.append(label)

sample['predict'] = predict

print(sample)

#dot_convertor.export(tree,"output/tree/zenit4")