class Graph:

    def __init__(self, nodeList, edgeList):
        self.nodeList = nodeList
        self.edgeList = edgeList

class Node:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Edge:
    def __init__(self, firstNode, secondNode):
        self.firstNode = firstNode
        self.secondNode = secondNode

class LocationNode(Node):

    def __init__(self, value, longitude, latitude):
        Node.__init__(self, value)
        self.longitude = longitude
        self.latitude = latitude
    
    def __str__(self):
        return Node.__str__(self)

class WeightedEdge(Edge):

    def __init__(self, firstNode, secondNode, value):
        Edge.__init__(self, firstNode, secondNode)
        self.value = value