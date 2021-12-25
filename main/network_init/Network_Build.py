from Constant import no_of_clients
from Entity import HostEntity, ClientEntity
from Show_Geographic import runGeographic
from Show_Network import runNetwork
from Show_Tree import runTree



Host = HostEntity()
ClientArray = []
for i in range(no_of_clients):
    ClientArray.append(ClientEntity(i))

runGeographic(Host, ClientArray)
# runNetwork(Host, ClientArray)
runTree(Host,ClientArray)

