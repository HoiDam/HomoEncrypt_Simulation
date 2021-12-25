from binarytree import Node
from operator import itemgetter
import collections
from drawtree import draw_level_order

def runTree(Host,ClientArray):    
    
    removed = []
    q, result = collections.deque(), []

    q.append(-1)
    result.append(-1)
    
    while q:
        for _ in range(len(q)):
            id = q.popleft()
            if id == -1:
                origin = Host.getLocation()
            else:
                origin = ClientArray[id].getLocation()
            
            print(id)
            rank = []
            for client in ClientArray:
                if client.getID() not in removed:
                    rank.append({"id": client.getID(),"distance":cal_distance(origin,client.getLocation())})
            rank.sort(key=itemgetter("distance"))
            
            if len(rank)>0:
                remove_node = rank.pop(0)["id"]
                result.append(remove_node)
                removed.append(remove_node)
                if len(rank)>0:
                    q.append(remove_node)

            if len(rank)>0:
                remove_node = rank.pop(0)["id"]
                result.append(remove_node)
                removed.append(remove_node)
                if len(rank)>0:
                    q.append(remove_node)
        
    print(result)

    print(draw_level_order(arraySerializer(result)))


def cal_distance(originArray,targetArray):
    return ((originArray[0] - targetArray[0])**2 + (originArray[1] - targetArray[1])**2 )**0.5 

def arraySerializer(array):
    string = "["
    string += ",".join(str(x) for x in array)
    string += "]"
    return string