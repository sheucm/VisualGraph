from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.core.serializers.json import DjangoJSONEncoder
import requests
import json
import psycopg2
# Create your views here.


def get_real_dengue_by_date(request):
	# date1, date2, gte default 0
	if request.method != 'GET':
		return HttpResponse(status=400)

	date1 = request.GET.get('date1', '')
	date2 = request.GET.get('date2', '')
	gte60 = request.GET.get('gte60', 'f')

	conn = psycopg2.connect("dbname='tainan_dengue' user='chengmao' host='50.112.161.185' password='netdb'")
	cur = conn.cursor()
	if date1 != '' and date2 != '' and gte60 != 'f':
		cur.execute("SELECT lon,lat,date,age from real_dengue where age='>60' and date BETWEEN {0} and {1}".format(date1,date2))
	elif date1 != '' and date2 != '':
		cur.execute('SELECT lon,lat,date,age from real_dengue where date BETWEEN {0} and {1}'.format(date1, date2))
	elif gte60 != 'f':
		cur.execute("SELECT lon,lat,date,age from real_dengue where age='>60'")
	else:
		cur.execute('SELECT lon,lat,date,age from real_dengue')
		
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return HttpResponse(json.dumps(rows, cls=DjangoJSONEncoder), status=200, content_type="application/json")


def weight_of_SSB(request):
	return HttpResponse(status=200)

