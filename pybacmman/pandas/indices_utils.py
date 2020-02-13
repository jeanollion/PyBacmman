# bacmman indices (barcode) manipulation
getParent = lambda indices : '-'.join(indices.split('-')[:-1])
getFrame = lambda indices : int(indices.split('-')[0])
def getPrevious(currentIndices):
    spl = currentIndices.split('-')
    spl[0] = str(int(spl[0])-1)
    return '-'.join(spl)
def getNext(currentIndices):
    spl = currentIndices.split('-')
    spl[0] = str(int(spl[0])+1)
    return '-'.join(spl)
def setFrame(indices, newFrame):
    spl = indices.split('-')
    spl[0] = str(newFrame)
    return '-'.join(spl)
