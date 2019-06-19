import configparser

from flask import Flask

app = Flask(__name__)

@app.route('/Gw/Init',methods=['POST'])
def Init():
    pass

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    configDef = config['DEFAULT']
    app.config['SERVER_NAME'] = configDef['url']
    app.run(debug=True)