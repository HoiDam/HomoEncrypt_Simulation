from flask import Flask, request
import json 

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def index():
    return 'CLI Reporting Server'
 
@app.route('/print',methods=['POST'])
def printing():
    print(request.json["msg"])
    return json.dumps({"success":True})

@app.route("/host_up",methods=['GET'])
def host_up():
    print("[+] - Host Instance Up")
    return json.dumps({"success":True})

@app.route("/client_up/<id>",methods=['GET'])
def client_up(id):
    print("[+] - Client Instance {} Up".format(str(id)))
    return json.dumps({"success":True})

app.run(host= "127.0.0.3", port= 3000, debug=True, threaded=True)