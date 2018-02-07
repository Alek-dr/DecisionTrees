from numpy import log2
from numpy import nan, inf

def enthropy(df,S,states):
    entr = 0
    n = df.shape[0]
    for i in states:
        ds = df[df[S]==i]
        m = ds.shape[0]
        if n!=0 and m!=0:
            j = log2(m/n)
            if j not in (nan, inf, -inf):
                entr+=(m/n)*j
    return -entr



