import configparser
import os
import re
import sys

from flask import Flask

from ConditionManager import ConditionManager
from Examiner import Examiner

sys.path.append(os.path.abspath('../CrossInfra'))
from Combination import Combination

app = Flask(__name__)

combLst = []
@app.route('/Gw/Init', methods=['POST'])
def Init():
    global combLst
    calc_regex = re.compile(r'([a-z][a-z]+[0-9,_,-]+)')
    ss_regex = re.compile(r'([s,o,c][0-9]+)')
    cm = ConditionManager()
    condLst = cm.readFromFile()
    #ex = Examiner()
    #newcondLst = ex.ParseCondition(condLst)

    comb = Combination()
    comb.InitCombinations()
    combLst = comb.GetCombinationLst()

    for comb in combLst:
        for cond in condLst:
            calcLst = calc_regex.findall(cond)
            ssLst = ss_regex.findall(cond)
            for calcItem in calcLst:
                vals = calcDef(calcItem, comb)
            for ssItem in ssLst:
                vals = calcBar(ssItem, comb)


def calcBar(exp,comb):
    if "o" in exp:
        num = str(exp).replace("o", "")
    elif "c" in exp:
        num = str(exp).replace("c", "")
    else:
        num = exp[:len(exp) - 1]
        num = str(num).replace("s", "")
    return scan([num, num], comb[0])

def calcDef(exp,comb):
    op = re.search(r'([a-z]+)', exp)
    exp = exp.replace(op[0], "")
    elements = exp.split("_")

    values = []
    for g in elements:
        if "-" in g:
            values = values + scan(g.split("-"), comb[0])
        else:
            values = values + scan([g, g], comb[0])
    return values


def scan(expRange, currCombination):
    values = []
    barIndex = 0
    expRange = list(map(int, expRange))

    for val in currCombination:
        if type(val) == list:
            actRange = [val[0], val[-1]]
            if actRange[0] > expRange[1]:
                break
            if expRange[0] <= actRange[0] <= expRange[1]:
                values.append((barIndex, barIndex+(len(val)-1)))
            barIndex += len(val)
        else:
            if int(expRange[0]) <= val <= int(expRange[1]):
                values.append(barIndex)
            elif val > int(expRange[1]):
                break
            barIndex += 1
    return values



def reverseTranslateOp(opNum):
    if opNum == str(6):
        return 'c'
    if opNum == str(5):
        return 'o'
    if opNum == str(4):
        return 'tmax'
    if opNum == str(1):
        return 'tmin'
    if opNum == str(3):
        return 'max'
    if opNum == str(2):
        return 'min'
    if opNum == str(3):
        return 'hmin'
    if opNum == str(2):
        return 'lmax'

def translateOp(opName):
    opName = opName[0]
    if opName == "c":
        return str(6)
    if opName == "o":
        return str(5)
    if opName == 'tmax':
        return str(4)
    if opName == 'tmin':
        return str(1)
    if opName == 'max':
        return str(3)
    if opName == 'min':
        return str(2)
    if opName == 'hmin':
        return str(3)
    if opName == 'lmax':
        return str(2)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    configDef = config['DEFAULT']
    app.config['SERVER_NAME'] = configDef['url']
    app.run(debug=True)
