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

class main_sim(arcade.Window):
    def __init__(self,Host,ClientArray):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT+100, "Geographic")
        arcade.set_background_color(arcade.color.BEIGE)

        self.Host = Host
        self.ClientArray = ClientArray

    def on_draw(self):
        
        arcade.start_render()

        x,y = self.Host.getLocation()
        self.drawEntity(x, y, HOST_TEXT, arcade.color.RED)
        for client in self.ClientArray:
            x,y = client.getLocation()
            self.drawEntity(x,y, str(client.getID()),arcade.color.BLUE)

    def drawEntity(self,x,y,text,color):
        arcade.draw_circle_outline(x, y, CIRCLE_SIZE, color, CIRCLE_BORDER_WIDTH,NUM_SEGMENTS)
        arcade.draw_text(text,
                        x + CIRCLE_SIZE + TEXT_TOOLTIP_ADD, 
                        y + CIRCLE_SIZE + TEXT_TOOLTIP_ADD,
                        color,
                        DEFAULT_FONT_SIZE,
                        width=CIRCLE_SIZE,
                        align="left")

def runGeographic(Host,ClientArray):
    print(Host.getLocation())
    for Client in ClientArray:
        print(Client.getLocation())

    main_sim(Host,ClientArray)
    arcade.run()