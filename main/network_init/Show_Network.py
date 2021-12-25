from pyvis.network import Network

def runNetwork(Host,ClientArray):
    g = Network()
    x,y = Host.getLocation()
    g.add_node(-1,value=10,title="HOST",x = x , y = y, label="HOST", color="#FF0000")

    for client in ClientArray:
        x,y = client.getLocation()
        g.add_node(client.getID(),value=10,title=str(client.getID()),x = x , y = y, label=str(client.getID()), color="#00FFFF")

    g.show('visualized_network.html')