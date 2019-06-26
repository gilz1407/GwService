import itertools
from operator import itemgetter
import Helper

combinationsLst = []
class Combination:
    constants = []

    def __init__(self):
        self.constants = [3, 5, 7, 9]
        self.dynamicBarMap = {'first': [3, 4, 5, 6], 'sec': [8, 9, 10, 11, 12, 13, 14],
                        'third': [16, 17, 18, 19, 20], 'four': [22, 23, 24, 25, 26, 27, 28, 29, 30, 31]}
        self.countCombination = {'first': [1, 2, 3, 4], 'sec': [1, 2, 3, 4, 5, 6, 7],
                            'third': [1, 2, 3, 4, 5], 'four': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

        self.finalLst = [0, 1, 2, [], 7, [], 15, [], 21, [], 32, 33]

        self.temp = self.finalLst[:]


    def InitCombinations(self):
        if len(combinationsLst) == 0:
            self.GenerateCombination()
        return combinationsLst

    def GenerateCombination(self):
        y = 0
        for x in list(itertools.product(self.countCombination['first'],self.countCombination['sec'], self.countCombination['third'], self.countCombination['four'])):
            self.finalLst[self.constants[0]] = self.CreateSequence(x, 0, self.dynamicBarMap['first'])
            self.finalLst[self.constants[1]] = self.CreateSequence(x, 1, self.dynamicBarMap['sec'])
            self.finalLst[self.constants[2]] = self.CreateSequence(x, 2, self.dynamicBarMap['third'])
            self.finalLst[self.constants[3]] = self.CreateSequence(x, 3, self.dynamicBarMap['four'])
            temp = self.finalLst
            combinationsLst.append([temp[:],Helper.listLength(temp),[[],[],[],[],[],-1],[]]) #combination tuple(items,graph details,conditions)

            y += 1

        print('\n'.join(map(str,combinationsLst)))
        print("total ", y)

    def CreateSequence(self,combination,counter,lst):
        survivals=[]
        for item in range(0, combination[counter]):
            survivals.append(lst[item])
        return survivals

    @classmethod
    def GetCombinationLst(cls):
        return sorted(combinationsLst, key=itemgetter(1), reverse=False)

    @classmethod
    def GetConstans(cls):
        return cls.constants