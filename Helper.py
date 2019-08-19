def listLength(lst):
    totalLength=0
    for item in lst:
        if (type(item)==list):
            totalLength+=len(item)
        else:
            totalLength+=1
    return totalLength

def lengthMapping(lst):
        prevItem = None
        temp = lst[:]
        lenDic={}
        refend = -1
        while len(temp) > 0:
            citem = temp.pop()
            if prevItem != citem[1] and prevItem is not None:
                lenDic[prevItem] = len(lst)+refend+1
            refend -= 1
            if len(temp) == 0:
                lenDic[citem[1]] = len(lst)+refend+1
            prevItem = citem[1]
        return lenDic