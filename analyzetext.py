# -*- coding: utf-8 -*-
import urllib,urllib2

cadena = "Sé que el linaje humano está destinado a retroceder más y más en la noche de los tiempos primitivos, antes de que vuelva a iniciarse la ascensión sangrienta hacia aquello que llamamos la civilización."
url = 'http://localhost:8000/?'
query = 'q='+urllib.unquote(cadena)
response = urllib2.urlopen(url+query)
json = response.read()
print json