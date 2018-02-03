from general.graph import Graph

G = Graph()

G.add_edge([0,1])
G.add_edge([1,3])
G.vertices = 4
G.delete_edge([2,1])

for e in G.edges:
    print(e)