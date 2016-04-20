from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.core.serializers.json import DjangoJSONEncoder
from alg.alg.greedy import Greedy
from alg.alg.mon import Montecarlo
from alg.alg.ran import Random
from random import randint
import timeit
import os
import psycopg2
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Create your views here.
def __pg_connect():
	conn = None
	with open (os.path.join(BASE_DIR, 'config.json'), 'r') as cfile:
		conn = psycopg2.connect(cfile.read())
	return conn

def algorithm(request):
	if request.method != 'GET':
		return HttpResponse(status=400)

		# Variables Sets
	method = request.GET.get('method', 'r')
	table = request.GET.get('table', 'dengue_population')
	max_nodes = int(request.GET.get('max_nodes', '5'))
	iteration = int(request.GET.get('iteration', '100'))
	
	# Constant Var
	DELETED_FIG = 5469

	max_weight = -1
	max_area = []

	
	if method == 'g':
		aOb = Greedy(table = table)
	elif method == 'm':
		aOb = Montecarlo(table = table)
	else: # method == 'r'
		aOb = Random(table = table)


	start = timeit.default_timer()

	for i in range(iteration):
		seed = DELETED_FIG
		while seed == DELETED_FIG:
			seed = randint(1,12765)
		
		if method == 'g':
			area = aOb.find_max_area(aOb.gernerate_area(seed=seed, MAX_NODES=max_nodes))
		elif method == 'm':
			area = aOb.find_max_area(aOb.generate_area(seed=seed, MAX_NODES=max_nodes))
		else: # method == 'r'
			area = aOb.generateArea(seed=seed, MAX_NODES=max_nodes)

		if aOb.size(area) > max_weight:
			max_weight = aOb.size(area)
			max_area = area
			print('{0},{1}'.format(max_weight,max_area))
	stop = timeit.default_timer()
	runtime = stop-start
	print ('Runtime: {0} seconds'.format(runtime))

	# 1-Neighbors 2-Neighbors
	neighbors1 = aOb.neighbors(max_area)
	neighbors2 = aOb.neighbors(max_area + neighbors1)

	response = dict({"max_area": max_area, "neighbors1":neighbors1, "neighbors2":neighbors2})
	return HttpResponse(json.dumps(response,cls=DjangoJSONEncoder), status=200, content_type='application/json')


