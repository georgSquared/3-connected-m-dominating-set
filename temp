import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_node(1)

G.add_nodes_from(range(2,8))

Vetrices = [8,9,10]

G.add_nodes_from(Vetrices)

print "Nodes of G "
print G.nodes()

G.add_edge(1,2)

e = (3,4)

G.add_edge(*e)

print "Edges of G"
print G.edges()

#G = nx.petersen_graph()

conn = 1

while conn<3:
	G= nx.gnm_random_graph(10, 20)
	conn = nx.node_connectivity(G) 


print "Nodes of G "
print G.nodes()

print "Edges of G"
print G.edges()

print "Connectivity of G is %d"%(nx.node_connectivity(G))

D = nx.dominating_set(G)
print "Dominators"
print D

nx.draw(G)
plt.show()


