from py4j.java_gateway import JavaGateway, GatewayParameters # requires py4j
from py4j.java_collections import ListConverter
from py4j.protocol import Py4JNetworkError

def saveAndOpenSelection(df, dsName:str, objectClassIdx:int, selectionName:str, showObjects:bool=False, showTracks:bool=False, openSelection:bool=False, objectClassIdxDisplay:int=-1, interactiveObjectClassIdx:int=-1, port=25335, python_proxy_port:int=25334, address='127.0.0.1', gateway_parameters={}):
    """Stores a selection to bacmman using python gateway (py4j). Bacmman must be running with an active python gateway server.

    Parameters
    ----------
    df : pandas DataFrame
        each line of the DataFrame is one element of the selection, defined by columns Indices & Position
    dsName : str
        bacmman dataset name to store the selection to.
    objectClassIdx : int
        index of the object class of the elements of the selection in the bacmman dataset
    selectionName : str
        name of the selection
    showObjects : bool
        whether contours of objects should be shown
    showTracks : bool
        whether track links of objects should be shown
    openSelection : bool
        whether the first kymograph of the selection should be open
    objectClassIdxDisplay : int
        if openSelection is true, object class idx of the opened kymograph
    interactiveObjectClassIdx : int
        if openSelection is true, interactive object class idx
    python_proxy_port : int
        python port of the java gateway
    """
    gateway = JavaGateway(python_proxy_port=python_proxy_port, gateway_parameters=GatewayParameters(address=address, port=port, **gateway_parameters))
    try:
        idx = ListConverter().convert(df.Indices.tolist(), gateway._gateway_client)
        pos = ListConverter().convert(df.Position.tolist(), gateway._gateway_client)
        gateway.saveCurrentSelection(dsName, objectClassIdx, selectionName, idx, pos, showObjects, showTracks, openSelection, False, objectClassIdxDisplay, interactiveObjectClassIdx)
    except Py4JNetworkError:
        print("Could not connect, is BACMMAN started?")
