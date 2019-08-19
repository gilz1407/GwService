import configparser
import json
import os
import re
from flask import Flask
from ConditionManager import ConditionManager
from Combination import Combination
from Helper import lengthMapping, listLength
from RedisConnection import connect

r = connect()
app = Flask(__name__)
configDef = None
combLst = []
@app.route('/Gw/Init', methods=['POST'])
def Init():
    global combLst
    calc_regex = re.compile(r'([a-z][a-z]+[0-9,_,-]+)')
    ss_regex = re.compile(r'([s,o,c][0-9]+)')
    condLst = ConditionManager().readFromFile()

    comb = Combination()
    comb.InitCombinations()
    combLst = comb.GetCombinationLst()

    r.delete("lengthMap")
    r.set("lengthMap", json.dumps(lengthMapping(combLst)))

    for cindx,comb in enumerate(combLst):
        condTempLst = condLst[:]
        for idx, cond in enumerate(condTempLst):
            calcLst = calc_regex.findall(cond)
            ssLst = ss_regex.findall(cond)
            for calcItem in calcLst:
                vals = calcDef(calcItem, comb)
                condTempLst[idx] = re.sub(r'\b' + re.escape(calcItem) + r'\b',"Calc("+str(vals)+","+"barsLst)", condTempLst[idx])
            for ssItem in ssLst:
                vals = calcBar(ssItem, comb)
                condTempLst[idx] = re.sub(r'\b' + re.escape(ssItem) + r'\b', "Calc("+str(vals)+","+"barsLst)", condTempLst[idx])
        comb.append(condTempLst)
        print(str(cindx))
    dict = {"tl": str(combLst)}
    r.set(configDef['publishOn'], json.dumps(dict))
    print("I'm ready!")
    return ""

def calcBar(exp, comb):
    result = ""
    part = ""
    if "o" in exp:
        num = str(exp).replace("o", "")
        result += "o"
    elif "c" in exp:
        num = str(exp).replace("c", "")
        result += "c"
    else:
        num = exp[:len(exp) - 1]
        part = exp[-1]
        num = str(num).replace("s", "")
        result += "s"
    res = scan([num, num], comb[0])
    return [res[0], part]

def calcDef(exp, comb):
    op = re.search(r'([a-z]+)', exp)
    exp = exp.replace(op[0], "")
    elements = exp.split("_")

    values = []
    for g in elements:
        if "-" in g:
            values = values + scan(g.split("-"), comb[0])
        else:
            values = values + scan([g, g], comb[0])
    return [values, op[0]]


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
                for i in range(barIndex, barIndex+(len(val)-1)+1):
                    values.append(i)
            barIndex += len(val)
        else:
            if int(expRange[0]) <= val <= int(expRange[1]):
                values.append(barIndex)
            elif val > int(expRange[1]):
                break
            barIndex += 1
    return values

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    configDef = config['DEFAULT']
    app.config['SERVER_NAME'] = os.getenv("Gw_HOST")
    r.delete(configDef['publishOn'])
    Init()
    app.run(debug=False)
