from flask import Flask, request

import json 
import threading
import arcade

from Constant import max_X, max_Y, min_X, min_Y



DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 10

CIRCLE_SIZE = 15
CIRCLE_BORDER_WIDTH = 3
NUM_SEGMENTS = -1

TEXT_TOOLTIP_ADD = 1

HOST_TEXT = "HOST"

SCREEN_WIDTH = max_X + min_X
SCREEN_HEIGHT = max_Y + min_Y

TEXT_TEMPLATE = "[{},{}]"

class main_sim(arcade.Window):
    def __init__(self,Host,ClientArray):
        self.Host = Host
        self.ClientArray = ClientArray

    def on_draw(self):
        self.clear()
        arcade.start_render()
        x,y = self.Host.getLocation()
        self.drawEntity(x, max_Y - y, HOST_TEXT, arcade.color.RED)
        for client in self.ClientArray:
            x,y = client.getLocation()
            self.drawEntity(x,max_Y - y, str(client.getID()),arcade.color.BLUE)

    def drawEntity(self,x,y,text,color):
        arcade.draw_circle_outline(x, y, CIRCLE_SIZE, color, CIRCLE_BORDER_WIDTH,NUM_SEGMENTS)
        arcade.draw_text(text,
                        x + CIRCLE_SIZE + TEXT_TOOLTIP_ADD, 
                        y + CIRCLE_SIZE + TEXT_TOOLTIP_ADD,
                        color,
                        DEFAULT_FONT_SIZE,
                        width=CIRCLE_SIZE,
                        align="left")
        arcade.draw_text(TEXT_TEMPLATE.format((x),str(y)),
                            x + CIRCLE_SIZE + TEXT_TOOLTIP_ADD, 
                            y - CIRCLE_SIZE - TEXT_TOOLTIP_ADD,
                            color,
                            DEFAULT_FONT_SIZE,
                            width=CIRCLE_SIZE,
                            align="left")        
    def changeColor(self):
        arcade.set_background_color(arcade.color.BLACK)

    def run(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT+100, "Geographic")
        arcade.set_background_color(arcade.color.BEIGE)
        arcade.run()
# --- 

def server():
    app = Flask(__name__)

    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    cache = {"consumed":0}

    @app.route('/')
    def index():
        simulation.changeColor()
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

    app.run(host= "127.0.0.3", port= 3000, threaded=True)

def visual(simulation):
    # simulation.changeColor()
    simulation.run()

def runGUI_Model(Host,ClientArray,connections):
    global simulation
    simulation = main_sim(Host,ClientArray)

    t1 = threading.Thread(target=server)
    t2 = threading.Thread(target=visual,args=(simulation,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    
