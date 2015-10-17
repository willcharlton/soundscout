#!/usr/bin/env python

import pyonep, json
from flask import Flask

app = Flask(__name__)
app.debug = True

_1P = pyonep.onep.OnepV1()

AUTH_SSMaster = {'cik': '79dc7a6ef240a4d2de55504d3e2f2f5da3018619'}

@app.route("/")
def hello():
	info = _1P.info(AUTH_SSMaster, {'alias':''})
	aliases = info[1]['aliases']
	for rid in aliases:
		r = _1P.read(AUTH_SSMaster, rid, {}, defer=True)
	result = _1P.send_deferred(AUTH_SSMaster)
	for r in result:
		print(r)
			
	data_list = ''
	for rid in aliases:
		for r in result:
			# print(r)
			if r[0]['procedure'] == 'read' and\
				r[0]['arguments'][0] == rid:
				print("will", r[2])
				data_list+='<li>{0} - {1}</li>'.format(aliases[rid], r[2])
	page = """
<html>
	<body>
	<h1>Soundscout Data</h1></br>
	{0}
	</body>
</html>
""".format(data_list)
	return page

if __name__ == "__main__":
	app.run()
