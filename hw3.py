# This script implements the Dijkstra algorithm 
# using heap 
#
# The input is a text file naming 'graph'
# Format in the 'graph' file
# 	first line: <vertex number> <edge number> <source point>
# 	following lines(describe edges): <start point> <end point> <weight>
#
# 'test-graph.png' is an example graph 

import heapq

MAX_VERTEX = 100
MAX_DISTANCE = 0xffffffff

# matrix stores weight between points
matrix = []
for i in range(MAX_VERTEX):
    matrix.append([])
    for j in range(MAX_VERTEX):
        matrix[i].append(0)  # initialize to 0

visited = []  # record whether the point has been visited
distance = []  # record current calculated distance from the source point
path = []  # record the last point to this point on the path

def Dijkstra(n, s):
    h = []  # heap
    # initialization, expand from the source point
    for i in range(n):
        visited.append(False)
        distance.append(MAX_DISTANCE)
        path.append(-1)
        if matrix[s][i]>0 and i!=s:
            distance[i] = matrix[s][i]
            path[i] = s
            heapq.heappush(h, (distance[i], i))
    
    path[s] = s
    distance[s] = 0
    visited[s] = True
    
    # expand from the left points
    for i in range(1,n):
        min, u = heapq.heappop(h)         
        visited[u] = True
        for k in range(n):
            if (visited[k] == False):
                heapq.heappush(h, (distance[k], k))
            if (visited[k] == False) and (matrix[u][k]>0) and ((min+matrix[u][k])<distance[k]):
                distance[k] = min+matrix[u][k]
                path[k] = u
                
                

# print out the path from source(s) to v
def PrintPath(v, s):
    p = []
    while v!=s:
        p.append(v)
        v = path[v]
        
    p.append(v)
    p.reverse()  # reverse the points
    
    return p 
     
     
with open('graph', 'r') as f:
    num = f.readline().split()
    n = int(num[0])
    e = int(num[1])
    s = int(num[2])
    
    # read in data
    for line in f.readlines():
        num = line.split()
        matrix[int(num[0])][int(num[1])] = int(num[2])
 
    Dijkstra(n, s)
    
    for i in range(n):
        if i!=s:
            print 'Path:', PrintPath(i, s), 'Distance:', distance[i]

