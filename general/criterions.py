from numpy import log2, square, nan, inf

criterions = ['entropy','gain_ratio','gini']

def entropy(df,s,states):
    entr = 0
    n = df.shape[0]
    if isinstance(states,(int,float)):
        states = [states]
    for i in states:
        ds = df[df[s]==i]
        m = ds.shape[0]
        if n!=0 and m!=0:
            j = log2(m/n)
            if j not in (nan, inf, -inf):
                entr+=(m/n)*j
    return -entr

def gini(df,s,states):
    g = 1
    n = df.shape[0]
    if isinstance(states,(int,float)):
        states = [states]
    for i in states:
        ds = df[df[s]==i]
        m = ds.shape[0]
        if m!=0:
            g -= square(m/n)
    return g



