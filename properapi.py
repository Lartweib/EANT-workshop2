# https://127.0.0.1:3030/api/BARRIO/INMUEBLE/TIPO
from bs4 import BeautifulSoup
import requests
import unicodedata
from flask import Flask, json
from os import environ
from urllib.parse import urlencode

app = Flask(__name__)

@app.route('/')
def hello_flask():
    return 'Hola desde Flask :D'

@app.route('/api/<barrio>/<inmueble>/<tipo>')
def scrapeo(barrio,inmueble,tipo):
    propiedades = []

    #for para navegar paginas
    for i in range(100):
        url = "https://www.properati.com.ar/s/"+barrio+"/"+inmueble+"/"+tipo+"?page="+str(i)
        response = requests.get(url)
        response.encoding = "utf-8"
        html = response.text
        dom = BeautifulSoup(html, features = "html.parser")
    #debugger
        print(url)    
        print(i)
    
    #if para corroborar si hay o no resultados    
        if dom.find( attrs = { 'class' : 'StyledTitle-n9541a-4 bwJAej' } ) != None:
                 
            anuncios = dom.find_all( attrs = { 'class' : 'StyledCard-n9541a-1 ixiyWf' } )
    
    #for para extraer info de cada anuncio        
            for anuncio in anuncios:
                titulo = anuncio.find( attrs = { 'class' : 'StyledTitle-n9541a-4 bwJAej' } )
                precio = anuncio.find( attrs = { 'class' : 'StyledPrice-sc-1wixp9h-0 bZCCaW' } )
                expensas = anuncio.find( attrs = { 'class' : 'StyledMaintenanceFees-n9541a-6 cRsmn' } )
                detalles = anuncio.find( attrs = { 'class' : 'StyledInfoIcons-n9541a-9 fgcFIO' } )
                inmobiliaria = anuncio.find( attrs = { 'class' : 'seller-name' } )
    
    #guarda la info en diccionario            
                dict = {}
                
                if titulo: dict['titulo'] = titulo.get_text()
                if precio: dict['precio']= precio.get_text()
                if expensas: dict['expensas'] = unicodedata.normalize("NFKD", expensas.get_text()) 
                if inmobiliaria: dict['imobiliaria'] = inmobiliaria.get_text()
                if detalles:
                    spans = detalles.find_all('span')
                    for span in spans:
                        txt = span.get_text()
                        if (txt.find('m²')>=0): dict['m2'] = txt
                        if (txt.find('ambiente')>=0): dict['ambientes'] = txt
                        if (txt.find('baño')>=0): dict['baño'] = txt
    
    #agrega a la lista las propiedades            
                propiedades.append(dict)
                
        else: break
    
    if len(propiedades) == 0:
        response = {'status' : 'error',
                    'rta' : 'no se encuentra el resultado'
                    }
        
    else: 
        response = app.response_class(response = json.dumps(propiedades), status= 200, mimetype = 'application/json')    
    
    return response
        

if __name__ == '__main__':
    app.run( port = 3030)#, host = '0.0.0.0' )








# #########Scrapeo#########

# propiedades = []

# #for para navegar paginas
# for i in range(100):
#     url = "https://www.properati.com.ar/s/palermo/departamento/alquiler?page="+str(i)
#     response = requests.get(url)
#     response.encoding = "utf-8"
#     html = response.text
#     dom = BeautifulSoup(html, features = "html.parser")
# #debugger
#     print(url)    
#     print(i)

# #if para corroborar si hay o no resultados    
#     if dom.find( attrs = { 'class' : 'StyledTitle-n9541a-4 bwJAej' } ) != None:
             
#         anuncios = dom.find_all( attrs = { 'class' : 'StyledCard-n9541a-1 ixiyWf' } )

# #for para extraer info de cada anuncio        
#         for anuncio in anuncios:
#             titulo = anuncio.find( attrs = { 'class' : 'StyledTitle-n9541a-4 bwJAej' } )
#             precio = anuncio.find( attrs = { 'class' : 'StyledPrice-sc-1wixp9h-0 bZCCaW' } )
#             expensas = anuncio.find( attrs = { 'class' : 'StyledMaintenanceFees-n9541a-6 cRsmn' } )
#             detalles = anuncio.find( attrs = { 'class' : 'StyledInfoIcons-n9541a-9 fgcFIO' } )
#             inmobiliaria = anuncio.find( attrs = { 'class' : 'seller-name' } )

# #guarda la info en diccionario            
#             dict = {}
            
#             if titulo: dict['titulo'] = titulo.get_text()
#             if precio: dict['precio']= precio.get_text()
#             if expensas: dict['expensas'] = unicodedata.normalize("NFKD", expensas.get_text()) 
#             if inmobiliaria: dict['imobiliaria'] = inmobiliaria.get_text()
#             if detalles:
#                 spans = detalles.find_all('span')
#                 for span in spans:
#                     txt = span.get_text()
#                     if (txt.find('m²')>=0): dict['m2'] = txt
#                     if (txt.find('ambiente')>=0): dict['ambientes'] = txt
#                     if (txt.find('baño')>=0): dict['baño'] = txt

# #agrega a la lista las propiedades            
#             propiedades.append(dict)
            
#     else: break

# ###########        
        
    
    
    
