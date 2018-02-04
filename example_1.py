from general.structures import BinaryTree, Node
import pandas as pd
from algorithms import learnID3
from preprocess.convert import convert_categorial
import os


data_set = pd.read_csv('datasets/zenit.csv')

data_set, fcc = convert_categorial(data_set)

learnID3.fit(data_set,'win')



