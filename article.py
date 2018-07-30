import pandas as pd
from trees.decison_trees import DecisonTree
from sklearn.model_selection import KFold
from general import dot_convertor

import time

data_set = pd.read_csv('datasets/Iris.csv')
data_set.drop("Id",axis=1,inplace=True)

kfold = KFold(n_splits=2, shuffle=True, random_state=0)

X = data_set.iloc[:,0:3]
y = data_set.iloc[:,4]

average_accuracy = 0
exec_time = 0

for train_index, test_index in kfold.split(X):

    X_train, X_test = X.iloc[train_index,:], X.iloc[test_index,:]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    train = pd.concat([X_train, y_train], axis=1)
    test = pd.concat([X_test, y_test], axis=1)

    tree = DecisonTree()

    start_time = time.clock()
    exec_time = 0

    tree.learnC45(train, 'Species', criteria='D')
    exec_time += time.clock() - start_time

    right = 0

    for i, row in test.iterrows():
        true_label = row['Species']
        label = tree.predict(row)
        if label==true_label:
            right+=1
    accuracy = right/test.shape[0]

    dot_convertor.export(tree, "d_iris")
    print('Accuracy = {:.3f}'.format(accuracy))
    average_accuracy += accuracy

print('Average accuracy = {:.3f}'.format(average_accuracy/kfold.get_n_splits()))
print('Average time = {:.3f}'.format(exec_time/kfold.get_n_splits()))




