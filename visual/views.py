from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.core.serializers.json import DjangoJSONEncoder
from alg.views import __pg_connect
from alg.views import algorithm
import requests
import json


# Create your views here.



def index(request):
	return render(request, 'index.html')

def get_real_dengue_by_date(request):
	# date1, date2, gte default 0
	if request.method != 'GET':
		return HttpResponse(status=400)

	date1 = request.GET.get('date1', '')
	date2 = request.GET.get('date2', '')
	gte60 = request.GET.get('gte60', 'f')

	conn = __pg_connect()
	cur = conn.cursor()
	
	if date1 != '' and date2 != '' and gte60 != 'f':
		cur.execute("SELECT lon, lafrom real_dengue where age='>60' and date BETWEEN '{0}' and '{1}'".format(date1,date2))
	elif date1 != '' and date2 != '':
		cur.execute("SELECT lon, lat from real_dengue where date BETWEEN '{0}' and '{1}'".format(date1, date2))
	elif gte60 != 'f':
		cur.execute("SELECT lon, lat from real_dengue where age='>60'")
	else:
		cur.execute("SELECT lon, lat from real_dengue")
		
	rows = cur.fetchall()
	conn.close()

	response = dict({"points":rows})
	return HttpResponse(json.dumps(response,cls=DjangoJSONEncoder), status=200, content_type='application/json')

def get_SSB(request):
	if request.method != 'GET':
		return HttpResponse(status=400)

	ogc_fid = 1  # Example
	
	method = request.GET.get('method', 'r')
	table = request.GET.get('table', 'dengue_population')
	max_nodes = int(request.GET.get('max_nodes', '5'))
	iteration = int(request.GET.get('iteration', '100'))

	req = requests.get('http://127.0.0.1:8000/alg/algorithm?method={0}&table={1}&max_nodes={2}&iteration={3}'
		.format(method,table,max_nodes,iteration))
	req_json = json.loads(req.text)
	max_area = req_json['max_area']
	neighbors1_area = req_json['neighbors1']
	neighbors2_area = req_json['neighbors2']

	conn = __pg_connect()
	cur = conn.cursor()

	ssblist = max_area #+ neighbors1_area + neighbors2_area

	# ogc_fid, geo, centroid
	cur.execute("SELECT O.ogc_fid, D.num_of_dengue, st_asgeojson(wkb_geometry), st_astext(st_centroid(wkb_geometry)) from ogrgeojson O, {0} D where O.ogc_fid in {1} and O.ogc_fid=D.ogc_fid"
		.format(table, tuple(ssblist)))
	rows = cur.fetchall()
	conn.close()

	features = list()
	for row in rows: # row: ogc_fid, num_of_dengue, wkb_geom, centroid(lng,lat)
		centroid = row[3][6:-1].split(' ')   # lng, lat

		feature = dict({
			"type":"Feature",
			"geometry": json.loads(row[2]),
			"properties":{
				"ogc_fid":row[0], 
				"weight": row[1],
				"centroid":{
					"lng":centroid[0], 
					"lat":centroid[1]
				}
			}
		})
		features.append(feature)

	response = dict({"type":"FeatureCollection", "features":features})
	return HttpResponse(json.dumps(response,cls=DjangoJSONEncoder), status=200, content_type='application/json')


def weight_of_SSB(request):
	if request.method != 'GET':
		return HttpResponse(status=400)
	return HttpResponse(status=200)

def get_neighbors(requests):
	if request.method != 'GET':
		return HttpResponse(status=400)
	ogc_fid_list = request.GET.get('ogc_fid_list', '')
	print (ogc_fid_list)

	return HttpResponse(status=200)


