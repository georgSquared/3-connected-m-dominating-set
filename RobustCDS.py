import networkx as nx
import matplotlib.pyplot as plt

def create_3():
	conn = 1

	while conn<3:
		G= nx.gnm_random_graph(10, 20)
		conn = nx.node_connectivity(G)

	return G


G = create_3()
print "Connectivity of G is %d"%(nx.node_connectivity(G))
