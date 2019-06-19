import configparser

from flask import Flask

from ConditionManager import ConditionManager
from Examiner import Examiner

app = Flask(__name__)

@app.route('/Gw/Init',methods=['POST'])
def Init():
    cm = ConditionManager()
    condLst = cm.readFromFile()
    ex = Examiner()
    ex.ParseCondition(condLst)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    configDef = config['DEFAULT']
    app.config['SERVER_NAME'] = configDef['url']
    app.run(debug=True)