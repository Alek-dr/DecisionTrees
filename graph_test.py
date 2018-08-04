from general.structures import Graph

g = Graph()

for i in range(8):
    g.add_vertex(i)

edges = [[0,1],[0,5],[0,6],[1,2],[2,3],[1,4],[6,7]]
for edg in edges:
    g.add_edge(edg)

print(g.vertices)
print(g.edges)

print(g.get_rel_depth(5))