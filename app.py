#!/usr/bin/env python
# coding=utf-8
import requests
import urllib2
import json
import os
from flask import Flask
from flask import request
from flask import make_response
from bs4 import BeautifulSoup 


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
		if (producto=="hogar"):
			url = "https://www.sura.com/soluciones-personas/seguro-hogar.aspx"
			r = urllib2.urlopen(url).read()
			soup = BeautifulSoup(r, 'html5lib')
			contenido = soup.find_all("div",class_="textRightColumn")
			speech = contenido[0]
			
		else:
       			speech = "Buscando informacion del producto " + producto
        
    	elif req.get("result").get("action") == "planes.salud":
        	url = "https://api.segurossura.com.co/public/v1/directory/products"
        	myResponse = requests.get(url)

        	if(myResponse.ok):
			jData = json.loads(myResponse.text)
			
		speech = "Seguros Sura Colombia ofrece los siguientes planes de salud: \n"
		
        	for plan in jData:
	       		speech = speech + "\n" + plan["nombreField"].title()
			
	elif req.get("result").get("action") == "info.especialistas":
		producto = parameters.get("plan-salud")
		ciudad = parameters.get("ciudad")
		especialidad = parameters.get("especialidad")
		
		url = "https://api.segurossura.com.co/public/v1/directory/search/" + producto + "/" + ciudad + "?speciality=" + especialidad + "&firstname=&secondname=&firstlastname=&secondlastname="
		myResponse = requests.get(url)

		if(myResponse.ok):
			jData = json.loads(myResponse.text)
		
		speech = "Los profesionales que coinciden con tu busqueda son: \n"

		for medico in jData:
	       		speech = speech + "\n" + medico["nombreField"] + "\n Direccion: " + medico["direccionField"].title() + "\n Telefono: " + medico["telefonoField"] + "\n"
			
	elif req.get("result").get("action") == "coberturas.producto":
		producto = parameters.get("productos")
		speech = "Buscando coberturas del producto: " + producto
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
