from flask import Flask, render_template, request, Response, redirect
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route("/")
def mainWebsite():
    try:
        with open('httplogs.json', 'r') as fin:
            datahttp = json.load(fin)
    except IOError:
        print('File not found, will create a new one.')
        datahttp = []
    try:
        with open('honeypotlogs.json', 'r') as fin:
            datahoneypot = json.load(fin)
    except IOError:
        print('File not found, will create a new one.')
        datahoneypot = [{"honeypots": []}]
    httpnum = len(datahttp)
    honeypotnum = len(datahoneypot)
    return render_template("index.html", httpnum=httpnum, honeypotnum=honeypotnum)


@app.route("/viewhttp")
def viewhttpLogs():
    try:
        with open('httplogs.json', 'r') as fin:
            datahttp = json.load(fin)
    except IOError:
        print('File not found, will create a new one.')
        datahttp = []
    finaldata = datahttp
    return render_template("httplogs.html", data=finaldata)


@app.route("/viewhoneypot")
def viewhoneypotLogs():
    try:
        with open('honeypotlogs.json', 'r') as fin:
            datahoneypot = json.load(fin)
    except IOError:
        print('File not found, will create a new one.')
        datahoneypot = [{"honeypots": []}]
    print(datahoneypot)
    finaldata = datahoneypot
    return render_template("honeypotlogs.html", data=finaldata)


@app.route("/httplogs", methods=["POST"])
def httpLogs():
    data2 = request.get_json()
    print(data2)
    try:
        with open('httplogs.json', 'r') as fin:
            data = json.load(fin)
    except IOError:
        print('File not found, will create a new one.')
        data = list()
    with open('httplogs.json', 'w') as fout:
        data.append(data2)
        json.dump(data, fout)
    return ("Data successfully Sent")


@app.route("/honeypotlogs", methods=["POST"])
def honeypotLogs():
    data2 = request.get_json()
    try:
        with open('honeypotlogs.json', 'r') as fin:
            data = json.load(fin)
    except IOError:
        print('File not found, will create a new one.')
        data = list()
    data.append(data2)
    with open('honeypotlogs.json', 'w') as fout:
        json.dump(data, fout)
    return ("Data successfully Sent")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
