# bacmman indices (barcode) manipulation
def getParent(indices):
    split = indices.split('-')[:-1]
    if len(split)==1:
        return int(split[0])
    else:
        return '-'.join(split)
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
