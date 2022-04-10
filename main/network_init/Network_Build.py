from Constant import no_of_clients
from Entity import HostEntity, ClientEntity
from Show_Geographic import runGeographic
from Show_Network import runNetwork
from Show_Tree import runTree
from Instantiate_Entity import runInstances

from GUI import runGUI_Model

import threading
import time

Host = HostEntity()
ClientArray = []
for i in range(no_of_clients):
    ClientArray.append(ClientEntity(i))

# runGeographic(Host, ClientArray)
aggregation_tree = runTree(Host,ClientArray)
connections = runNetwork(Host, ClientArray,aggregation_tree)
print(connections)

# ---

def logic(Host, ClientArray,connections):
    time.sleep(5)
    runInstances(Host, ClientArray,connections)

def visual(Host, ClientArray,connections):
    runGUI_Model(Host, ClientArray,connections)

t1 = threading.Thread(target=logic, args=(Host, ClientArray,connections,))
t2 = threading.Thread(target=visual, args=(Host, ClientArray,connections,))

t1.start()
t2.start()

t1.join()
t2.join()