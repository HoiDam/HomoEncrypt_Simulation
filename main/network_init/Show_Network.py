from pyvis.network import Network

RED = "#FF0000"
BLUE = "#00FFFF"

def runNetwork(Host,ClientArray,aggregation_tree):
    g = Network(height='100%', width='100%')
    x,y = Host.getLocation()
    g.add_node(-1,title="HOST",x = x , y = y, label="HOST", color=RED , physics = False)

    for client in ClientArray:
        x,y = client.getLocation()
        g.add_node(client.getID(),title=str(client.getID()),x = x , y = y, label=str(client.getID()), color=BLUE , physics = False)

    # --- Transfer to 2d array --
    two_d_tree = []
    i = 0
    layer = []
    while aggregation_tree:
        layer.append(aggregation_tree.pop(0))
        if len(layer) == 2**i:
            two_d_tree.append(layer)
            i+=1
            layer = []
    if layer:
        two_d_tree.append(layer)
    # print(two_d_tree)
    # ---------------------------
    

    connections = {}
    for layer in range(len(two_d_tree)-1,0,-1):
        for child_id in range(len(two_d_tree[layer])):
            # print(two_d_tree[layer][child_id], two_d_tree[layer-1][child_id//2])
            g.add_edge(two_d_tree[layer][child_id], two_d_tree[layer-1][child_id//2] , physics = False)
            
            if two_d_tree[layer-1][child_id//2] not in connections:
                connections[two_d_tree[layer-1][child_id//2]] = []
            connections[two_d_tree[layer-1][child_id//2]].append(two_d_tree[layer][child_id])

    g.show('visualized_network.html')
    return connections