def listLength(lst):
    totalLength=0
    for item in lst:
        if (type(item)==list):
            totalLength+=len(item)
        else:
            totalLength+=1
    return totalLength