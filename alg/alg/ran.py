import networkx as nx
import psycopg2
from random import shuffle
from random import randint
from datetime import datetime
import sys
import timeit
from os.path import expanduser
import json


class Random:
	def __init__(self, table):
		self.G = nx.Graph()
		self.init_G(table)
	def init_G(self, table):
		conn = psycopg2.connect("dbname='tainan_dengue' user='ubuntu' host='50.112.161.185' port='5432' password='netdb'")
		cur = conn.cursor()
		cur.execute("""SELECT ogc_fid, neighbors from neighborhood""")
		rows_neighbors = cur.fetchall()

		# Build the edges according to spatial unit neighbors
		for neighbor in rows_neighbors:
			touch_ids = neighbor[1].split(',')[:-1]
			ogc_fid = neighbor[0]
			for t_id in touch_ids:
				self.G.add_edge(ogc_fid, int(t_id))

		# Set the weight of nodes
		cur.execute("SELECT ogc_fid, num_of_dengue from {0}".format(table))
		rows_dengue = cur.fetchall()
		for row in rows_dengue:
			self.G.add_node(row[0], weight=row[1])
		conn.close()


	def neighbors(self, subgraph_nodes):
		union = {}
		for node in subgraph_nodes:
			union = set(union) | set(self.G.neighbors(node))
		return list( set(union)-set(subgraph_nodes) )
	def size(self, subgraph_nodes):
		total_weight = 0
		subgraph = self.G.subgraph(subgraph_nodes)
		for node in subgraph.nodes():
			total_weight += self.G.node[node]['weight']
		return total_weight
	def generateArea(self, seed, MAX_NODES):
		area = [seed]
		while len(area) < MAX_NODES :	
			neigs = self.neighbors(area)
			if len(neigs) == 0:
				break
			i = randint(0,len(neigs)-1)
			area = area + [neigs[i]]
		return area


if __name__ == "__main__":
	if len(sys.argv) != 4:
		print ("USAGE: [TABLE:(e.g.:dengue_population)] [MAX] [ITERATION]")
		sys.exit(0)

	# Variables Sets
	TABLE = sys.argv[1]
	MAX = int(sys.argv[2])
	ITERATION = int(sys.argv[3])
	
	# Constant Var
	DELETED_FIG = 5469

	max_weight = -1

	rOb = Random(TABLE)

	start = timeit.default_timer()

	for i in range(ITERATION):
		seed = DELETED_FIG
		while seed == DELETED_FIG:
			seed = randint(1,12765)

		area = rOb.generateArea(seed=seed, MAX_NODES=MAX)
		if rOb.size(area) > max_weight:
			max_weight = rOb.size(area)
			print('{0},{1}'.format(max_weight,area))

	stop = timeit.default_timer()
	print ('Runtime: {0} seconds'.format(stop-start))
