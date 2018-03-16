from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.tree import export_graphviz
import pandas as pd

#iris = load_iris()
from preprocess.convert import convert_categorial

data_set = pd.read_csv('datasets/zenit.csv')
data_set.drop("day",axis=1,inplace=True)
feature_names = data_set.columns[0:4]
target_names = ['no','yes']
tree = DecisionTreeClassifier(random_state=0, criterion='gini')
#df, _ = convert_categorial(data_set)
target = data_set['win'].values
data = data_set.loc[:, data_set.columns != 'win'].as_matrix()
tree.fit(data, target)

export_graphviz(tree,
                out_file="cart_zenit.dot",
                feature_names=feature_names,
                class_names=target_names,
                rounded=True,
                filled=True)