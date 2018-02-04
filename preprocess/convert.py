import pandas as pd
import numpy as np
import numbers


def categorial2code(df,target):
    t_labels = df[target].unique()
    class_code = {}
    for i, l in enumerate(t_labels):
        class_code[l] = i
    for i in range(df.shape[0]):
        label = df.loc[i][target]
        df.loc[i, target] = class_code[label]
    return df, class_code

def convert_categorial(df):
    feature_class_code = {}
    for col in df:
        if not df[col].dtype in (int, float, complex):
            f_labels = df[col].unique()
            class_code = {}
            for i, l in enumerate(f_labels):
                class_code[l] = i
            feature_class_code[col] = class_code

            for i in range(df.shape[0]):
                label = df.loc[i][col]
                df.loc[i, col] = class_code[label]
    return df, feature_class_code


