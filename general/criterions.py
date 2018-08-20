from numpy import log2, square, nan, inf, sqrt

criterions = ['entropy','gain_ratio','gini','D']

#region Splitting criterions

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
        ds = df[df[s] == i]
        m = ds.shape[0]
        if m!=0:
            g -= square(m/n)
    return g

def D(df,attribute,target,states):
    d = 0
    if isinstance(states,(int,float)):
        states = [states]
    for s in states:
        sub = df[df[attribute] == s]
        df = df[df[attribute] != s]
        if df.empty:
            break
        for _,row in sub.iterrows():
            diff = (df[target]!=row[target])
            d += diff[diff==True].shape[0]
    return d

def D_continous(df,attribute,target,trsh):
    d = 0
    sub = df[df[attribute] <= trsh]
    df = df[df[attribute] > trsh]
    if not df.empty:
        for _,row in sub.iterrows():
            diff = (df[target]!=row[target])
            d += diff[diff==True].shape[0]
    return d

#endregion

#region pruning estimations

def est_err(f,z,n):
    num = f + (z**2)/(2*n) + z*sqrt((f/n) - ((f**2)/n) + ((z**2)/(4*n**2)))
    den = 1 + (z**2)/n
    return round(num/den,2)



