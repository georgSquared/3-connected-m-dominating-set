import sys
import networkx as nx
import matplotlib.pyplot as plt
from tarjan import biconnected_component_edges

#Create a random graph until it is 3-connected
def create_3():
	conn = 1

	while conn<3:
		G= nx.gnm_random_graph(20, 40)
		conn = nx.node_connectivity(G)

	return G

#Compute a CDS, based on algorithm of Butenko, Cheng, Oliveira, Pardalos
def computeCDS(G):

	#Temporary copy of graph
	graphD = G.copy()

	#Current CDS in D
	D = G.nodes()
	print "Initial D"
	print D

	#Current fixed vetrices in F
	F = []

	neighbourhood = []

	for i in range(0, nx.number_of_nodes(G)):
		neighbourhood.append(len(G.neighbors(i)))

	print "Neighbourhood "
	print neighbourhood

	print "Index of min value is",
	print neighbourhood.index(min(neighbourhood))

	#Mpakalis
	minimum = 99999
	maximum = -1

	while (set(D) - set(F)):

		#Mpakalis
		minimum = 99999
		maximum = -1

		#find min number of neighbours
		for i in (set(D) - set(F)):
			if neighbourhood[i] < minimum:
				minimum = neighbourhood[i]
				u = i

		#u = neighbourhood.index(minimum)

		print "D is ",
		print D

		print "u is",
		print u

		tempG = graphD.copy()
		tempG.remove_node(u)

		if not nx.is_connected(tempG):
			F.append(u)
		else:
			D.remove(u)

			#Error correction
			if not nx.is_dominating_set(G, D):
				print "Error, reverting D and exiting"
				D.append(u)
				break

			#graphD = tempG.copy()
			graphD.remove_node(u)
			#adjust neighbours
			for node in D:
				if node in G.neighbors(u):
					neighbourhood[node] = neighbourhood[node] - 1


			if not set(G.neighbors(u)).intersection(F):
				for i in G.neighbors(u):
					if neighbourhood[i] > maximum:
						maximum = neighbourhood[i]
						w = i

				#w = neighbourhood.index(maximum)
				F.append(w)
		
		print "F is",
		print F


	return D


def compute_1_connected_k_dominating_set(G, CDS):

	MIScandidates = []
	add_flag = True

	MIScandidates.append(CDS[0])

	for i in range(1, len(CDS)):
		for j in range(0, len(MIScandidates)):
			if G.has_edge(CDS[i], MIScandidates[j]):
				add_flag = False
				break
		if add_flag:
			MIScandidates.append(CDS[i])

	#print "MIScandidates"
	#print MIScandidates

	MIS = nx.maximal_independent_set(G, MIScandidates)
	#print "Maximal Independent Set"
	#print MIS

	C = list(set(CDS) - set(MIScandidates))
	#print "C is",
	#print C

	newCDS = MIS
	#print newCDS

	for i in C:
		newCDS.append(i)

	CDSGraph = G.subgraph(newCDS)

	if not (nx.is_dominating_set(G, newCDS) and nx.is_connected(CDSGraph)):
		print "Error, C and I did not create a CDS"
		sys.exit()

	I1 = MIS

	newG = G.copy()

	newG.remove_nodes_from(I1)

	I2 = nx.maximal_independent_set(newG)

	#Union of sets
	DA = list(set(I1) | set(I2) | set(C))

	return DA

def compute_2_connected_k_dominating_set(G, DA):

	graphDA = G.subgraph(DA)

	DB = DA

	B = biconnected_component_edges(graphDA)



G = create_3()
print "Connectivity of G is %d"%(nx.node_connectivity(G))

print "\n"

print "Nodes of G "
print G.nodes()

print "Edges of G"
print G.edges()

print "\n"

CDS = computeCDS(G)

print "\n"

print "CDS"
print CDS

if nx.is_dominating_set(G, CDS):
	print "Succesfull Connected Dominating Set"
else:
	print "ERROR, did not achieve Connected Dominating Set"

print "\n"

CDS = compute_1_connected_k_dominating_set(G, CDS)
print "1-connected 3-dominating set"
print CDS

CDS = compute_2_connected_k_dominating_set(G, CDS)
print "2-connected 3-dominating set"
print CDS

#GraphCDS = G.subgraph(CDS)

#print "Is the graph connected?"
#print nx.is_connected(GraphCDS)

#print biconnected_component_edges(GraphCDS)


