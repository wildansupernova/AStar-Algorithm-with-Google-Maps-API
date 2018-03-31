from Graph import *
import math

activeBranches = []
edgeList = []

heuristicDistance = lambda x, y :None

def EuclideanDistance(node, goalNode):
    return math.sqrt((node.latitude - goalNode.latitude)**2 +(node.longitude - goalNode.longitude)**2)

def HarversineDistance(node, goalNode):
    lat1 = node.latitude
    lat2 = goalNode.latitude
    lon1 = node.longitude
    lon2 = goalNode.longitude
    R = 6371 # earth radius , assumption: the earth is like sphere or ball, mountains not counted or other else curve
    theta1 = lat1 * math.pi / 180
    theta2 = lat2 * math.pi / 180
    ohm1 = lon1 * math.pi / 180
    ohm2 = lon2 * math.pi / 180
    
    r1x = R*math.cos(theta1)*math.cos(ohm1)
    r1y = R*math.cos(theta1)*math.sin(ohm1)
    r1z = R*math.sin(theta1)

    r2x = R*math.cos(theta2)*math.cos(ohm2)
    r2y = R*math.cos(theta2)*math.sin(ohm2)
    r2z = R*math.sin(theta2)
    d = math.sqrt(((r1x-r2x)*(r1x-r2x)) + ((r1y-r2y)*(r1y-r2y)) + ((r1z-r2z)*(r1z-r2z)))
    #Keluaran dalam meter
    return round(d*1000)

def ShortestPath(currBranch, goalNode):
    global activeBranches, heuristicDistance, edgeList
    currPath, currCost = currBranch
    currNode = currPath[-1]
    # remove current branch from active branches
    activeBranches.remove(currBranch)
    # current node is not goal node
    if(currNode != goalNode):
        # add to active branches every branch node from current node
        for edge in edgeList:
            if edge.firstNode == currNode:
                activeBranches.append((currPath + [edge.secondNode], currCost + edge.value))
        # get the branch which last node has the minimum heuristic distance to the goal node
        minBranch = min(activeBranches, key= lambda x: (heuristicDistance(x[0][-1], goalNode) + x[1]))
        # call recursive of this function from the minimum branch
        return ShortestPath(minBranch, goalNode)
    else:
        # return solution
        return currPath

def GetShortestPath(startNode, goalNode):
    global heuristicDistance, activeBranches
    heuristicDistance = EuclideanDistance
    currBranch = ([startNode], 0)
    activeBranches = [currBranch]
    return ShortestPath(currBranch, goalNode)

def SetEdgeList(iedgeList):
    global edgeList
    edgeList = iedgeList
        