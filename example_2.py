from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.tree import export_graphviz

iris = load_iris()

tree = DecisionTreeClassifier(random_state=0, criterion='entropy')

tree.fit(iris.data, iris.target)

export_graphviz(tree,
                out_file="my_zenit_tree.dot",
                feature_names=iris.feature_names[:],
                class_names=iris.target_names,
                rounded=True,
                filled=True)