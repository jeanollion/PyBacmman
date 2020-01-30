from py4j.java_gateway import JavaGateway # requires py4j
from py4j.java_collections import ListConverter
from py4j.protocol import Py4JNetworkError

def saveAndOpenSelection(df, dsName, objectClassIdx, selectionName, showObjects=False, showTracks=False, open=False, openWholeObjectClassIdx=False, objectClassIdxDisplay=-1, interactiveObjectClassIdx=-1):
    gateway = JavaGateway()
    java = gateway.entry_point
    try:
        idx = ListConverter().convert(df.Indices.tolist(), gateway._gateway_client)
        pos = ListConverter().convert(df.Position.tolist(), gateway._gateway_client)
        gateway.saveCurrentSelection(dsName, objectClassIdx, selectionName, idx, pos, showObjects, showTracks, open, openWholeObjectClassIdx, objectClassIdxDisplay, interactiveObjectClassIdx)
    except Py4JNetworkError:
        print("Could not connect, is BACMMAN started?")
