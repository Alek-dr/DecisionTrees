import pandas as pd
from trees.decison_trees import DecisonTree
from general import dot_convertor

data_set = pd.read_csv('datasets/PlayTennis.csv')

tree = DecisonTree()

data_set.drop("Day",axis=1,inplace=True)
sample = data_set.copy()
print(data_set)
params = {'criteria':'entropy','max_depth':2}
tree.learnC45(data_set,'Play',params)

# tree.learnC45(data_set,'Play', criteria='D')
#
# for i,row in sample.iterrows():
#     label = tree.predict(row)
#     print('{} {}'.format(i+1,label))

dot_convertor.export(tree,"output/tree/tennis2")