import networkx as nx
import matplotlib.pyplot as plt

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

	print "Index of min value"
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



	


G = create_3()
print "Connectivity of G is %d"%(nx.node_connectivity(G))

print "Nodes of G "
print G.nodes()

print "Edges of G"
print G.edges()

CDS = computeCDS(G)
print "CDS"
print CDS

if nx.is_dominating_set(G, CDS):
	print "Succesfull Connected Dominating Set"
else:
	print "ERROR, did not achieve Connected Dominating Set"
