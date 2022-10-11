from app import app
from flask.globals import request
from models.planeta import Planeta
from flask import render_template, request
import requests
import json

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/busca', methods=['GET', 'POST'])  # type: ignore
def busca():    
    planeta = Planeta(request.form['nome'].lower(), '', '')

    # BUSCA POR PAGINAÇAO
    for pagina in range(1, 7):
            res = requests.get("https://swapi.dev/api/planets/?page={}".format(pagina))
            result = json.loads(res.content.decode('utf-8'))
            planetas = result['results']

            for x in planetas:

                if planeta.nome == x['name'].lower():
                    
                    habitantes_planeta = []

                    for y in x['residents']:
                        res = requests.get(y)
                        result = json.loads(res.content.decode('utf-8'))
                        habitantes_planeta.append(result['name'])
                    
                    planeta.nome = x['name']
                
                    return render_template('index.html',
                        nome = planeta.nome,
                        residentes = habitantes_planeta)

    return render_template('erro.html')


@app.route('/about')
def about():
    return render_template('about.html',)