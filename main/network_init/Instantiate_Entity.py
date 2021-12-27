import threading
import requests
from flask import Flask, request

from Constant import ip_template,ip,client_port,host_port,cli_ip

def runInstances(Host, ClientArray,connections):

    # --- Client Instantiating -------------
    appArray = []
    for i in range(len(ClientArray)):
        app = Flask(__name__)
        @app.route('/')
        def index():
            id = int(request.host.split(":")[1]) - client_port
            return 'Client Instance ID: '+str(id)
        appArray.append(app)

    threadArray = []
    for i in range(len(appArray)):
        threadArray.append(threading.Thread(target=runFlaskApp_Client, args=(appArray,i,)))
    for i in range(len(threadArray)):
        threadArray[i].start()
        report_clientup(i)

    # ------------------------------------

    # --- Host Instantiating -------------
    app = Flask(__name__)
    @app.route('/')
    def index():
        return 'Host Instance'
    report_hostup()
    app.run(host = ip, port = host_port, debug=False, threaded=True)
    # ------------------------------------

def runFlaskApp_Client(appArray,i):
    appArray[i].run(host=ip, port=client_port+i, debug=False, threaded=True)   


def report_hostup():
    requests.get(cli_ip+"/host_up")


def report_clientup(id):
    requests.get(cli_ip+"/client_up/"+str(id))