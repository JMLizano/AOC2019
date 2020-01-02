from collections import defaultdict 
from part1 import read_input, process_orbit, space_collection, _INPUT_FILE

# Graph is represented using adjacency list. Every 
# node of adjacency list contains vertex number of 
# the vertex to which edge connects. It also contains 
# weight of the edge 
class Graph: 
    """ From: https://www.geeksforgeeks.org/shortest-path-for-directed-acyclic-graphs/"""
    def __init__(self,vertices): 
  
        self.V = vertices # No. of vertices 
  
        # dictionary containing adjacency List 
        self.graph = defaultdict(list) 
  
    # function to add an edge to graph 
    def addEdge(self,u,v,w): 
        self.graph[u].append((v,w)) 
  
  
    # A recursive function used by shortestPath 
    def topologicalSortUtil(self,v,visited,stack): 
  
        # Mark the current node as visited. 
        visited[v] = True
  
        # Recur for all the vertices adjacent to this vertex 
        if v in self.graph.keys(): 
            for node,weight in self.graph[v]: 
                if visited[node] == False: 
                    self.topologicalSortUtil(node,visited,stack) 
  
        # Push current vertex to stack which stores topological sort 
        stack.append(v) 
  
  
    ''' The function to find shortest paths from given vertex. 
        It uses recursive topologicalSortUtil() to get topological 
        sorting of given graph.'''
    def shortestPath(self, s): 
  
        # Mark all the vertices as not visited 
        visited = [False]*self.V 
        stack =[] 
  
        # Call the recursive helper function to store Topological 
        # Sort starting from source vertice 
        for i in range(self.V): 
            if visited[i] == False: 
                self.topologicalSortUtil(s,visited,stack) 
  
        # Initialize distances to all vertices as infinite and 
        # distance to source as 0 
        dist = [float("Inf")] * (self.V) 
        dist[s] = 0
  
        # Process vertices in topological order 
        while stack: 
  
            # Get the next vertex from topological order 
            i = stack.pop() 
  
            # Update distances of all adjacent vertices 
            for node,weight in self.graph[i]: 
                if dist[node] > dist[i] + weight: 
                    dist[node] = dist[i] + weight 
  
        # Print the calculated shortest distances 
        for i in range(self.V):
            print (" %d  ---> %d" % (i, dist[i])) if dist[i] != float("Inf") else  "Inf"


def main():
    orbits = read_input(input_file=_INPUT_FILE)
    [process_orbit(orbit) for orbit in orbits]
    g = Graph(len(space_collection.keys()))
    int_space_collection  = {s:i for i,s in enumerate(space_collection.keys()) }
    print(int_space_collection)
    for k in space_collection.keys():
        print(k, space_collection[k].orbiting)
        current_int = int_space_collection[k]
        if space_collection[k].orbiting != None:
            orbiting_int = int_space_collection[space_collection[k].orbiting]
            g.addEdge(current_int , orbiting_int, 1)
            g.addEdge(orbiting_int , current_int, 1)
    print(f"SANTA is {int_space_collection['SAN']}")
    print(f"Z3P is {int_space_collection['Z3P']}")
    g.shortestPath(int_space_collection['YOU'])


if __name__  == '__main__':
    main()