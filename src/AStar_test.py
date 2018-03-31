from Graph import *
from AStar import *

A = LocationNode(('A', 1, 4))
B = LocationNode(('B', 3, 4))
C = LocationNode(('C', 2, 2))
D = LocationNode(('D', 4, 2))
S = LocationNode(('S', 4, 1))
E1 = WeightedEdge(A, B, EuclideanDistance(A, B))
E2 = WeightedEdge(B, C, EuclideanDistance(B, C))
E3 = WeightedEdge(B, D, EuclideanDistance(B, D))
# E4 = WeightedEdge(B, S, euclideanDistance(B, S))
E5 = WeightedEdge(C, S, EuclideanDistance(C, S))
E6 = WeightedEdge(D, S, EuclideanDistance(D, S))

edgeList = [E1, E2, E3, E6, E5]
SetEdgeList(edgeList)
SetHeuristicDistanceFunc(EuclideanDistance)
solution = GetShortestPath(A, S)

for node in solution:
    print(node)