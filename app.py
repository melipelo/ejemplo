#!/usr/bin/env python
# coding=utf-8
import requests
import urllib
import json
import os
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
	res = makeWebhookResult(req)
    	res = json.dumps(res, indent=4)
    	print(res)
    	r = make_response(res)
    	r.headers['Content-Type'] = 'application/json'
    	return r

def makeWebhookResult(req):
	result = req.get("result")
	parameters = result.get("parameters")
	
	if req.get("result").get("action") == "productos.sura":
        	cliente = parameters.get("tipo_cliente")
        	speech = "Buscando productos para " + cliente
		
	elif req.get("result").get("action") == "producto.info":
        	producto = parameters.get("producto")
        	speech = "Buscando informacion del producto " + producto
        
    	elif req.get("result").get("action") == "planes.salud":
        	url = "https://api.segurossura.com.co/public/v1/directory/products"
        	myResponse = requests.get(url)

        	if(myResponse.ok):
			jData = json.loads(myResponse.text)
		speech = "Seguros Sura Colombia ofrece los siguientes planes de salud: \n"
        	for plan in jData:
	        	speech = speech + "\n" + plan["nombreField"].title()
	else:
        	speech =" "

	return {
        	"speech": speech,
        	"displayText": speech,
        	#"data": {},
        	# "contextOut": [],
        	"source": "apiai-onlinestore-shipping"
    	}


if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

    	print "Starting app on port %d" % port

    	app.run(debug=True, port=port, host='0.0.0.0')
