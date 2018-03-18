
def categorial2code(df,target):
    t_labels = df[target].unique()
    class_code = {}
    for i, l in enumerate(t_labels):
        class_code[l] = i
    for i in range(df.shape[0]):
        label = df.loc[i][target]
        df.loc[i, target] = class_code[label]
    return df, class_code

def convert_categorial(df,as_categories=[]):
    """
    :param df: Pandas dataframe.
    :param as_categories: list of columns names, which values have to be considered as categorical despite they are numerical.
    :return: df - same dataframe with converted features;
            feature_class_code - dictionary that contains corresponds between code and values of features.
    """
    feature_class_code = {}
    for col in df:
        if (not df[col].dtype in (int, float, complex)) or (col in as_categories):
            f_labels = df[col].unique()
            class_code = {}
            for i, l in enumerate(f_labels):
                class_code[l] = i
            feature_class_code[col] = class_code

            for i in range(df.shape[0]):
                label = df.loc[i][col]
                df.loc[i, col] = class_code[label]
    return df, feature_class_code


