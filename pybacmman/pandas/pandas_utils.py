import pandas as pd
from pandas import merge
from .indices_utils import getNextFrame, getPreviousFrame

def subsetByDataframe(df, dfSubset, on, sub_on=None, keepCols = []):
    """Return rows of dataframe df that are present in dfSubset

    Parameters
    ----------
    df : DataFrame
        DataFrame to subset
    dfSubset : DataFrame
        DataFrame used to define the subset
    on : list of Strings
        Column names to join on. These must be found in both DataFrames if sub_on is None.
    sub_on : list of Strings
        Column names to join on in the dfSubset DataFrame.
    keepCols : list of Strings
        columns of dfSubset that should be kept in resulting DataFrame

    Returns
    -------
    DataFrame
        subset of df

    """
    if sub_on is None:
        sub_on=on
        rem_cols=[]
    else:
        assert len(sub_on)==len(on), "sub_on should have same length as on"
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

def setSelectionEdges(dfSelection, left=True):
    """Create a boolean column that defines the edge of the selection (in terms of Frames). If left=True: value is True when there is no previous object. If left = false, value is True when there is no next object

    Parameters
    ----------
    dfSelection : DataFrame
        dataframe with a column SelectionName, Position & Indices
    left : boolean
        see summary

    Returns
    -------
    void
        inplace modification of dfSelection

    """
    colName = "LeftEdge" if left else "RightEdge"
    fun = getNextFrame if left else getPreviousFrame
    dfNeigh = pd.DataFrame({"SelectionName":dfSelection.SelectionName, "Position":dfSelection.Position, "Indices":dfSelection.Indices.apply(fun)})
    leftEdges = pd.concat([dfSelection[["SelectionName", "Position", "Indices"]], dfNeigh, dfNeigh]).drop_duplicates(keep=False)
    dfSelection[colName] = False
    dfSelection.loc[leftEdges.index, colName] = True
