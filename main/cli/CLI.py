from flask import Flask, request
import json 

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

cache = {"consumed":0}

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
    print("[+] - Node {} Up".format(str(id)))
    return json.dumps({"success":True})

@app.route('/child_consumed',methods=['POST'])
def child_consumed():
    jsonFile = request.json
    id = jsonFile["id"]
    consumed = jsonFile["consumed"]
    print("[+] - Node {} Consumed {} units ".format(str(id),str(consumed)))
    cache["consumed"] += consumed
    return json.dumps({"success":True})

@app.route('/total_consumed/cache',methods=['GET'])
def total_consumed_cache():
    print("[CLI_Cache] - Total Consumed {} units".format(str(cache["consumed"])))
    cache["consumed"] = 0
    print("\n=======================\n")
    return json.dumps({"success":True})

@app.route("/total_consumed/system_count",methods=['POST'])
def total_consumed_system_count():
    jsonFile = request.json
    print("[HE_HOST] - Total Consumed {} units".format(str(jsonFile["consumed"])))
    return json.dumps({"success":True})

@app.route('/contacting_to',methods=['POST'])
def contactingTo():
    jsonFile = request.json
    print("[?] - Node {} asking node {}".format(jsonFile["from"],jsonFile["to"]))
    return json.dumps({"success":True})

app.run(host= "127.0.0.3", port= 3000, debug=True, threaded=True)