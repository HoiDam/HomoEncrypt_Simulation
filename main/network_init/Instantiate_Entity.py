import threading
import requests
import random
import json
import time
from flask import Flask, request
from phe import paillier

from Constant import ip_template,ip,client_port,host_port,cli_ip

def runInstances(Host, ClientArray,connections):
    report_hostup() # fake host up
    # --- Client Instantiating -------------
    appArray = []
    for i in range(len(ClientArray)):
        app = Flask(__name__)
        @app.route('/')
        def index():
            id = int(request.host.split(":")[1]) - client_port
            return 'Client Instance ID: '+str(id)
        appArray.append(app)
        @app.route('/child_retrieve',methods=['GET'])
        def child_retrieve():
            public_key_json = requests.get(ip_template.format(ip,host_port)+'get_public_key').json()["public_key"]
            public_key = paillier.PaillierPublicKey(public_key_json["n"])

            id = int(request.host.split(":")[1]) - client_port
            consumed = random.randint(1,10) 
            report_child_consumed(id,consumed)
            time.sleep(2)

            if id in connections:
                for child in connections[id]:
                    report_contacting(id,child)
                    time.sleep(2)
                    consumed_json = requests.get(ip_template.format(ip,client_port+child)+'/child_retrieve').json()
                    consumed += cipherDeserializer(public_key,consumed_json) 
            else:
                consumed = public_key.encrypt(consumed)

            return cipherSerializer(public_key, consumed)

    threadArray = []
    for i in range(len(appArray)):
        threadArray.append(threading.Thread(target=runFlaskApp_Client, args=(appArray,i,)))
    for i in range(len(threadArray)):
        threadArray[i].start()
        report_clientup(i)
        time.sleep(1)

    # ------------------------------------

    # --- Host Instantiating -------------
    app = Flask(__name__)
    public_key, private_key = paillier.generate_paillier_keypair()
    @app.route('/')
    def index():
        return 'Host Instance'
    @app.route('/aggregation')
    def retrieve():
        consumed = 0
        id = -1
        for child in connections[id]:
            report_contacting(id,child)
            time.sleep(2)
            consumed_json = requests.get(ip_template.format(ip,client_port+child)+'/child_retrieve').json()
            consumed += cipherDeserializer(public_key,consumed_json) 
        consumed = private_key.decrypt(consumed)
        report_final(consumed)
        return json.dumps({"success":True})
    @app.route('/get_public_key',methods=['GET'])
    def get_public_key():
        return json.dumps({"public_key":
                            {
                                "g":public_key.g,
                                "n":public_key.n
                            }
        })
    # report_hostup()
    app.run(host = ip, port = host_port, debug=False, threaded=True)
    # ------------------------------------

def runFlaskApp_Client(appArray,i):
    appArray[i].run(host=ip, port=client_port+i, debug=False, threaded=True)   

def cipherSerializer(public_key, cipher):
    serialized_object = {}
    serialized_object['public_key'] = {'g': public_key.g, 'n': public_key.n}
    serialized_object['values'] = (str(cipher.ciphertext()), cipher.exponent)
    return json.dumps(serialized_object)

def cipherDeserializer(public_key, serialized_object):
    return paillier.EncryptedNumber(public_key, int(serialized_object['values'][0]), int(serialized_object['values'][1]))

# --- Report -----------
def report_hostup():
    requests.get(cli_ip+"/host_up")

def report_clientup(id):
    requests.get(cli_ip+"/client_up/"+str(id))

def report_child_consumed(id,consumed):
    jsonFile = {"id":id,"consumed":consumed}
    requests.post(cli_ip+"/child_consumed",json=jsonFile)

def report_final(consumed):
    jsonFile = {"consumed":consumed}
    requests.post(cli_ip+"/total_consumed/system_count",json = jsonFile)
    requests.get(cli_ip+"/total_consumed/cache")

def report_contacting(id,child):
    jsonFile = {"from":id,"to":child}
    requests.post(cli_ip+"/contacting_to",json = jsonFile)
# ----------------------