#!/usr/bin/env python

import pyonep, json
from flask import Flask, Markup, render_template
from datetime import datetime

app = Flask(__name__)
app.debug = True

_1P = pyonep.onep.OnepV1()

AUTH_SSMaster = {'cik': '79dc7a6ef240a4d2de55504d3e2f2f5da3018619'}

NUM_DATAPOINTS = 5
@app.route("/")
def main():
	info = _1P.info(AUTH_SSMaster, {'alias':''})
	aliases = info[1]['aliases']
	print("aliases", aliases)

	for rid in aliases:
		r = _1P.read(AUTH_SSMaster, rid, {'limit': NUM_DATAPOINTS}, defer=True)
	result = _1P.send_deferred(AUTH_SSMaster)
	
	data_rows = {}
	data_list = ''
	for rid in aliases:
		for r in result:
			if r[0]['procedure'] == 'read' and\
				r[0]['arguments'][0] == rid:
				print("will", r[2])
				data_rows[ aliases[rid][0] ] = [ r[2][d] for d in range(0, NUM_DATAPOINTS) ]
	return render_template('main.html', data_rows=data_rows)

@app.route("/map")
def map():
	info = _1P.info(AUTH_SSMaster, {'alias':''})
	aliases = info[1]['aliases']
	print("aliases", aliases)

	for rid in aliases:
		r = _1P.read(AUTH_SSMaster, rid, {'limit': NUM_DATAPOINTS}, defer=True)
	result = _1P.send_deferred(AUTH_SSMaster)
	
	data_rows = {}
	data_list = ''
	for rid in aliases:
		for r in result:
			if r[0]['procedure'] == 'read' and\
				r[0]['arguments'][0] == rid:
				print("will", r[2])
				data_rows[ aliases[rid][0] ] = [ r[2][d] for d in range(0, NUM_DATAPOINTS) ]
	return render_template('map.html', data_rows=data_rows)


@app.template_filter('dtime')
def dtime(ts):
	return datetime.fromtimestamp( int(ts) ).strftime("%H:%M:%S-%Y/%m/%d")

@app.template_filter('unjson')
def unjson(blob):
	print(blob)
	return Markup("""
<table>
<tr><td>Loudness</td><td>{0}</td></tr>
<tr><td>Airplane-ness</td><td>{1}</td></tr>
</table>
""".format(json.loads(blob)['amplitude'], 1000000*json.loads(blob)['airplane_ness']  ))

@app.template_filter('gps')
def gps(blob):
	location = '44.98014269999999,-93.28874739999999'
	if not json.loads(blob).get('location') == None:
		location = json.loads(blob).get('location')
	elif not json.loads(blob).get('address') == None:
		location = json.loads(blob).get('address')
	return [ float(i) for i in location.split(',') ]

if __name__ == "__main__":
	app.run(host = '0.0.0.0' if not app.debug else '127.0.0.1')




