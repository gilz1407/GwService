import re
import redis

class ConditionManager():
    def __init__(self):
        self.conditions = []

    def readFromFile(self):
        conditions = []
        lineIndex = -1
        file = open("./condition.txt")
        line = ""
        index = 2
        for tmp in file.readlines():
            lineIndex += 1
            startLineWith = re.search(r'(([0-9]+)[.]+(.*))', tmp)
            index = 2
            if startLineWith == None:
                startLineWith = re.search(r'(.*)', tmp)
                index = 0
            else:
                if lineIndex > 0:
                    self.conditions.append(line)
                    line = ""
                    startLineWith = re.search(r'(([0-9]+)[.]+(.*))', tmp)
                    index = 2
            line += " " + str(startLineWith.groups()[index])
            line = line.replace("||", " or ").replace("&&", " and ").replace("=<", "<=").replace("=>", ">=").replace(
                "\n", "")

        self.conditions.append(line)
        print("Read Line=%s" % self.conditions)
        return self.conditions
