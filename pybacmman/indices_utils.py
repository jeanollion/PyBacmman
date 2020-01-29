getParent = lambda s : '-'.join(s.split('-')[:-1])
def getPreviousFrame(currentIndices):
    spl = currentIndices.split('-')
    spl[0] = str(int(spl[0])-1)
    return '-'.join(spl)
def getNextFrame(currentIndices):
    spl = currentIndices.split('-')
    spl[0] = str(int(spl[0])+1)
    return '-'.join(spl)
