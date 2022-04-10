from turtle import color
from flask import Flask, request

import json 
import threading
import arcade

from Constant import max_X, max_Y, min_X, min_Y



DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 10
NARRATION_FONT_SIZE = 28
CONSUMPTION_FONT_SIZE = 15

CIRCLE_SIZE = 15
CIRCLE_BORDER_WIDTH = 3
NUM_SEGMENTS = -1

TEXT_TOOLTIP_ADD = 1

HOST_TEXT = "HOST"

SCREEN_WIDTH = max_X + min_X
SCREEN_HEIGHT = max_Y + min_Y

TEXT_TEMPLATE = "[{},{}]"

class main_sim(arcade.Window):
    def __init__(self,Host,ClientArray,connections):
        self.Host = Host
        self.ClientArray = ClientArray
        self.connections = connections
        self.narration = "Node Network is generating..."
        self.contacting = [-2,-2]

    def on_draw(self):
        self.clear()
        arcade.start_render()
        x,y = self.Host.getLocation()
        self.drawEntity(x, max_Y - y, HOST_TEXT, arcade.color.RED,self.Host.getStatus())
        for client in self.ClientArray:
            x,y = client.getLocation()
            self.drawEntity(x,max_Y - y, str(client.getID()),arcade.color.BLUE,client.getStatus())
            self.drawConsumption(x,max_Y - y,client.getConsumption())
        for key,value in self.connections.items():
            if key == -1:
                parent = self.Host
            else:
                parent = self.ClientArray[key]
            

            x1,y1 = parent.getLocation()
            status = parent.getStatus()
            for child in value:
                x2,y2 = self.ClientArray[child].getLocation()
                if (key == self.contacting[0] and child == self.contacting[1]):
                    color = arcade.color.RED
                else:
                    color = arcade.color.GREEN
                self.drawConnections(x1,y1,x2,y2,status,color)
        self.drawNarration(self.narration)

    def drawEntity(self,x,y,text,color,status):
        if status == "Offline":
            color = arcade.color.BLACK
        arcade.draw_circle_outline(x, y, CIRCLE_SIZE, color, CIRCLE_BORDER_WIDTH,NUM_SEGMENTS)
        arcade.draw_text(text,
                        x + CIRCLE_SIZE + TEXT_TOOLTIP_ADD, 
                        y + CIRCLE_SIZE + TEXT_TOOLTIP_ADD,
                        color,
                        DEFAULT_FONT_SIZE,
                        width=CIRCLE_SIZE,
                        align="left")
        # arcade.draw_text(status,
        #                     x + CIRCLE_SIZE + TEXT_TOOLTIP_ADD, 
        #                     y - CIRCLE_SIZE - TEXT_TOOLTIP_ADD,
        #                     color,
        #                     DEFAULT_FONT_SIZE,
        #                     width=CIRCLE_SIZE,
        #                     align="left")        
    
    def drawConnections(self,x1,y1,x2,y2,status,color):
        if status == "Online":
            arcade.draw_line(x1,max_Y - y1,x2,max_Y - y2,color,2)
    
    def drawNarration(self,text):
        arcade.draw_text(text,
                        SCREEN_WIDTH/100, 
                        SCREEN_HEIGHT,
                        arcade.color.BLACK,
                        NARRATION_FONT_SIZE,
                        width=SCREEN_WIDTH*99/100,
                        align="center")

    def drawConsumption(self,x,y,consumption):
        if consumption != 0:
            arcade.draw_text(str(consumption)+" kW",
                            x - 10* CIRCLE_SIZE,
                            y - CIRCLE_SIZE - TEXT_TOOLTIP_ADD,
                            arcade.color.BLACK,
                            CONSUMPTION_FONT_SIZE,
                            width=9* CIRCLE_SIZE,
                            align="right")

    def changeColor(self):
        arcade.set_background_color(arcade.color.BLACK)

    def run(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT+100, "Geographic")
        arcade.set_background_color(arcade.color.ALICE_BLUE)
        arcade.run()
    
    def changeHostStatus(self):
        self.Host.setStatusOnline()
    
    def changeClientStatus(self,id):
        self.ClientArray[id].setStatusOnline()

    def changeNarration(self,narration):
        self.narration = narration
    
    def changeClientConsumptions(self,id,consumption):
        self.ClientArray[id].setConsumption(consumption)

    def changeContacting(self,contacting):
        self.contacting = contacting
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
        simulation.changeHostStatus()
        return json.dumps({"success":True})

    @app.route("/client_up/<id>",methods=['GET'])
    def client_up(id):
        print("[+] - Node {} Up".format(str(id)))
        simulation.changeClientStatus(int(id))
        return json.dumps({"success":True})

    @app.route('/child_consumed',methods=['POST'])
    def child_consumed():
        jsonFile = request.json
        id = jsonFile["id"]
        consumed = jsonFile["consumed"]
        narration = "[+] - Node {} Consumed {} kW ".format(str(id),str(consumed))
        print(narration)
        simulation.changeNarration(narration)
        simulation.changeClientConsumptions(int(id),int(consumed))
        cache["consumed"] += consumed
        return json.dumps({"success":True})

    @app.route('/total_consumed/cache',methods=['GET'])
    def total_consumed_cache():
        print("[CLI_Cache] - Total Consumed {} kW".format(str(cache["consumed"])))
        cache["consumed"] = 0
        print("\n=======================\n")
        return json.dumps({"success":True})

    @app.route("/total_consumed/system_count",methods=['POST'])
    def total_consumed_system_count():
        jsonFile = request.json
        print("[HE_HOST] - Total Consumed {} kW".format(str(jsonFile["consumed"])))
        return json.dumps({"success":True})

    @app.route('/contacting_to',methods=['POST'])
    def contactingTo():
        jsonFile = request.json
        narration = "[?] - Node {} asking node {}".format(jsonFile["from"],jsonFile["to"])
        print(narration)
        simulation.changeNarration(narration)
        simulation.changeContacting([int(jsonFile["from"]),int(jsonFile["to"])])
        return json.dumps({"success":True})

    app.run(host= "127.0.0.3", port= 3000, threaded=True)

def visual(simulation):
    # simulation.changeColor()
    simulation.run()

def runGUI_Model(Host,ClientArray,connections):
    global simulation
    simulation = main_sim(Host,ClientArray,connections)

    t1 = threading.Thread(target=server)
    t2 = threading.Thread(target=visual,args=(simulation,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    
