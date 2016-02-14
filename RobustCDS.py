import sys
import networkx as nx
import matplotlib.pyplot as plt

#Create a random graph until it is 3-connected
def create_3(nodes, edges):
	conn = 1
	loop_count = 0

	while conn<3 and loop_count<1000:
		G= nx.gnm_random_graph(nodes, edges)
		conn = nx.node_connectivity(G)

		loop_count = loop_count + 1

	return G

#Compute a CDS, based on algorithm of Butenko, Cheng, Oliveira, Pardalos
def computeCDS(G):

	#Temporary copy of graph
	graphD = G.copy()

	#Current CDS in D
	D = G.nodes()
	#print "Initial D"
	#print D

	#Current fixed vetrices in F
	F = []

	neighbourhood = []

	for i in range(0, nx.number_of_nodes(G)):
		neighbourhood.append(len(G.neighbors(i)))

	#print "Neighbourhood "
	#print neighbourhood

	#print "Index of min value is",
	#print neighbourhood.index(min(neighbourhood))

	
	minimum = 99999
	maximum = -1

	while (set(D) - set(F)):

		
		minimum = 99999
		maximum = -1

		#find min number of neighbours
		for i in (set(D) - set(F)):
			if neighbourhood[i] < minimum:
				minimum = neighbourhood[i]
				u = i

		#u = neighbourhood.index(minimum)

		#print "D is ",
		#print D

		#print "u is",
		#print u

		tempG = graphD.copy()
		tempG.remove_node(u)

		if not nx.is_connected(tempG):
			F.append(u)
		else:
			D.remove(u)

			#Error correction
			if not nx.is_dominating_set(G, D):
				#print "Error, reverting D and exiting"
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
		
		#print "F is",
		#print F


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

	#Here we just construct a 3-dominating set
	#Could be a loop to m, for an m-dominating set
	newG = G.copy()

	newG.remove_nodes_from(I1)

	I2 = nx.maximal_independent_set(newG)

	#Union of sets
	DA = list(set(I1) | set(I2) | set(C))

	return DA

def compute_2_connected_k_dominating_set(G, DA):

	graphDA = G.subgraph(DA)

	DB = DA

	genB = nx.biconnected_components(graphDA)
	
	B = []
	for item in genB:
		B.append(list(item))

	#print "B"
	#print B

	art_points = list(nx.articulation_points(graphDA))
	#print "Articulation Points"
	#print art_points

	P = []

	while len(B)>1:


		for block in B:
			inducedL = list(set(block) - set(art_points))
			L = block

			#print "L"
			#print L
			#print "inducedL"
			#print inducedL

			if inducedL:
				break

		for v in inducedL:
			tempDB = list(DB)
			tempDB.remove(v)

			#Now for nodes in DA, may need DB
			for u in list(set(graphDA.nodes()) - set(L)):
				tempDB.remove(u)

				newG = G.copy()
				newG.remove_nodes_from(tempDB)

				#This part can make the algorithm fail
				if nx.has_path(newG, v, u):
					tempP = nx.shortest_path(newG, v, u)
					P.append(tempP)

		#print "P"
		#print P
		
		minPath = min(P, key=len)

		#Keep intermediate nodes of path
		interPath = list(minPath)
		interPath.pop(0)
		interPath.pop(-1)


		for node in interPath:
			DB.append(node)

		#Compute new CDS graph and recalculate B
		tempGraph = G.subgraph(DB)
		B = []
		for item in genB:
			B.append(list(item))

		genB = nx.biconnected_components(tempGraph)

		#print "B"
		#print B

		art_points = list(nx.articulation_points(tempGraph))
		#print "Articulation Points"
		#print art_points

	return DB

def compute_3_connected_k_dominating_set(G, D):

	graphCDS = G.subgraph(D) 

	if nx.node_connectivity(graphCDS)<2:
		print "Input is not 2-connected.Exiting"
		return D

	separators = list(nx.all_node_cuts(graphCDS))

	#print "separators"
	#print separators

	while separators and nx.node_connectivity(graphCDS)<3:

		broken = False

		discD = list(set(D) - separators[0])

		#print "discD"
		#print discD

		temp_graph_D = G.subgraph(discD)

		genD = nx.connected_components(temp_graph_D)

		components = list(genD)
		#print "Components"
		#print components

		for v in components[0]:

			tempD = list(D)
			tempD.remove(v)

			for u in components[1]:

				tempD.remove(u)

				newG = G.copy()
				newG.remove_nodes_from(tempD)

				if nx.has_path(newG, v, u):
					Hpath = nx.shortest_path(newG, v, u)

					#print "Hpath is",
					#print Hpath

					broken = True
					break

			if broken:
				break

		for node in Hpath:
			if node not in D:
				D.append(node)

		graphCDS = G.subgraph(D)
		separators = list(nx.all_node_cuts(graphCDS))

		#print "separators"
		#print separators

	return D

"""
START OF MAIN PROGRAM
"""

print "Please give number of desired nodes and edges"

N = int(raw_input("Nodes:"))
E = int(raw_input("Edges:"))

G = create_3(N, E)

while nx.node_connectivity(G)<3:
	print "Could not create 3-connected graph. Please consider increasing the edges"

	N = int(raw_input("Nodes:"))
	E = int(raw_input("Edges:"))

	G = create_3(N, E)

#nx.draw(G)
#plt.show()

print "Connectivity of G is %d"%(nx.node_connectivity(G))

print "\n"

print "Nodes of G "
print G.nodes()

print "Edges of G"
print G.edges()

print "\n"

position = nx.fruchterman_reingold_layout(G)

nx.draw_networkx_nodes(G, position, nodelist=G.nodes(), node_color="y")

nx.draw_networkx_edges(G,position)
nx.draw_networkx_labels(G,position)

#plt.show()
plt.savefig("1_initial.png")


CDS = computeCDS(G)

print "\n"

print "CDS"
print CDS

#G1 = G.subgraph(CDS) 
#nx.draw(G1)
#plt.show()

if nx.is_dominating_set(G, CDS):
	print "Succesfull Connected Dominating Set"
else:
	print "ERROR, did not achieve Connected Dominating Set"

print "\n"

#position = nx.fruchterman_reingold_layout(G)

#nx.draw_networkx_nodes(G,position, nodelist=G.nodes(), node_color="b")
nx.draw_networkx_nodes(G,position, nodelist=CDS, node_color="r")

#nx.draw_networkx_edges(G,position)
#nx.draw_networkx_labels(G,position)

plt.savefig("2_CDS.png")


CDS = compute_1_connected_k_dominating_set(G, CDS)
print "1-connected 3-dominating set"
print CDS

#G2 = G.subgraph(CDS) 
#nx.draw(G2)
#plt.show()

#position = nx.fruchterman_reingold_layout(G)

#nx.draw_networkx_nodes(G,position, nodelist=G.nodes(), node_color="b")
nx.draw_networkx_nodes(G,position, nodelist=CDS, node_color="r")

#nx.draw_networkx_edges(G,position)
#nx.draw_networkx_labels(G,position)

plt.savefig("3_1-conn_3-dom.png")




graphCDS = G.subgraph(CDS)

if not (nx.is_biconnected(graphCDS)):
	print "\n"
	CDS = compute_2_connected_k_dominating_set(G, CDS)
	print "2-connected 3-dominating set"
	print CDS
	print "\n"
else:
	print "Above set is also 2-connected"
	print "\n"

#position = nx.fruchterman_reingold_layout(G)

#nx.draw_networkx_nodes(G,position, nodelist=G.nodes(), node_color="b")
nx.draw_networkx_nodes(G,position, nodelist=CDS, node_color="r")

#nx.draw_networkx_edges(G,position)
#nx.draw_networkx_labels(G,position)

plt.savefig("4_2-conn_3-dom.png")


CDS = compute_3_connected_k_dominating_set(G, CDS)

G3 = G.subgraph(CDS)

if nx.node_connectivity(G3)>=3:
	print "3-connected 3-dominating set"
	print CDS
else:
	print "Failure. Final Result is not 3-connected"

#DRAWING TESTS

#position = nx.fruchterman_reingold_layout(G)

#nx.draw_networkx_nodes(G,position, nodelist=G.nodes(), node_color="b")
nx.draw_networkx_nodes(G,position, nodelist=CDS, node_color="r")

#nx.draw_networkx_edges(G,position)
#nx.draw_networkx_labels(G,position)

plt.savefig("5_3-conn_3-dom.png")

#GraphCDS = G.subgraph(CDS)

#print "Is the graph connected?"
#print nx.is_connected(GraphCDS)

#print biconnected_component_edges(GraphCDS)


