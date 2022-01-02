from Constant import no_of_clients
from Entity import HostEntity, ClientEntity
from Show_Geographic import runGeographic
from Show_Network import runNetwork
from Show_Tree import runTree
from Instantiate_Entity import runInstances

Host = HostEntity()
ClientArray = []
for i in range(no_of_clients):
    ClientArray.append(ClientEntity(i))

runGeographic(Host, ClientArray)
aggregation_tree = runTree(Host,ClientArray)
connections = runNetwork(Host, ClientArray,aggregation_tree)
# # print(connections)
runInstances(Host, ClientArray,connections)