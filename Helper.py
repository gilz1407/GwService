def listLength(lst):
    totalLength=0
    for item in lst:
        if (type(item)==list):
            totalLength+=len(item)
        else:
            totalLength+=1
    return totalLength


def lengthMapping(lst):
        prevItem = -1
        temp = lst[:]
        counter = 0
        lenDic={}
        sumFromLst = 0
        while len(temp) > 0:
            citem = temp.pop()
            if prevItem != citem[1]:
                if prevItem != -1:
                    sumFromLst += counter + 1
                    lenDic[prevItem] = len(lst) - sumFromLst
                prevItem = citem[1]
                counter = 0
            else:
                counter += 1
        print(lenDic)