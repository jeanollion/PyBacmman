from pandas import merge

def subsetByDataframe(df, dfSubset, on, sub_on=None, keepCols = []):
    if sub_on is None:
        sub_on=on
        rem_cols=[]
    else:
        rem_cols = [c+'_y' for c in sub_on if not c in on]
    if len(keepCols)==0:
        subcols = sub_on
    else:
        subcols = sub_on + keepCols
    dfSubset = dfSubset[subcols].drop_duplicates()
    res = merge(df, dfSubset, how='inner', left_on=on, right_on=sub_on, suffixes=('', '_y'))
    if len(rem_cols)>0:
        res.drop(rem_cols, 1, inplace=True)
    return res
