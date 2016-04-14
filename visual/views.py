from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.core.serializers.json import DjangoJSONEncoder
from alg.views import __pg_connect
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
		cur.execute("SELECT lon, lat from real_dengue where age='>60' and date BETWEEN '{0}' and '{1}'".format(date1,date2))
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
	#return HttpResponse(json.dumps(rows, cls=DjangoJSONEncoder), status=200, content_type="application/json")

def get_SSB(request):
	if request.method != 'GET':
		return HttpResponse(status=400)

	ogc_fid = 1  # Example
	conn = __pg_connect()
	cur = conn.cursor()

	cur.execute("SELECT codebase from ogrgeojson where ogc_fid={0}".format(ogc_fid))
	codebase = cur.fetchone()[0]
	cur.execute("SELECT * from neighborhood_codebase where codebase='{0}'".format(codebase))
	neighbors1 = cur.fetchone()[1]
	cur.execute("SELECT * from neighborhood_2deg_codebase where codebase='{0}'".format(codebase))
	neighbors2 = cur.fetchone()[1]

	cblist = [codebase] + neighbors1.split(',')[:-1] + neighbors2.split(',')[:-1]

	# ogc_fid, geo, centroid
	cur.execute("SELECT ogc_fid, st_asgeojson(wkb_geometry), st_astext(st_centroid(wkb_geometry)) from ogrgeojson where codebase in {0}".format(tuple(cblist)))
	rows = cur.fetchall()
	conn.close()

	features = list()
	for row in rows:
		centroid = row[2][6:-1].split(' ')   # lng, lat

		feature = dict({
			"type":"Feature",
			"geometry": json.loads(row[1]),
			"properties":{
				"ogc_fid":row[0], 
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





