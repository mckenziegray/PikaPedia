from flask import Flask, render_template, url_for, request
import os
import time
import sys
import whoosh
import os
import csv
import json
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from static.scripts.search_engine import *

app = Flask(__name__)

#Loads Single Page for individule pokemon
#
@app.route('/SinglePokemonLoadPage', methods=['GET', 'POST', 'pokemonInfo', 'query'])
def SinglePokemonLoadPage():
    if request.method == 'POST':
        data = request.form
    else:
        data = request.args
	
	#String passed into funciton form Homepage
    info = data.get('pokemonInfo')
	
    lengthInfo = len(info)

    info = json.loads(info.replace("'", '"'))

    return render_template('SinglePokemonLoadPage.html',
    #Variables for web page
        name=info['name'],
        id=int(info['id']),
        type_1=info['type_1'],
        type_2=info['type_2'],
        hp = info['hp'],
        attack = info['attack'],
        defense = info['defense'],
        sp_atk = info['sp_atk'],
        sp_def = info['sp_def'],
        speed = info['speed'],
        height = int(info['height']),
        weight = int(info['weight']),
        ability_1=info['ability_1'],
        ability_2=info['ability_2'],
        hidden_ability=info['ability_hidden'],
        moves=info['moves'],
        first_form=info['first_form'],
        second_forms=info['second_forms'],
        third_forms=info['third_forms'],
    )

#Loads Search Page for pokemon
@app.route('/', methods=['GET', 'POST'])
def PikaPediaHomepage():
    if request.method == 'POST':
        data = request.form
    else:
        data = request.args

	#Pages functionality
    page_num = data.get("page_num")
    if page_num is None:
        page_num = 1
        query = data.get('search_input')
    else:
        page_num = int(page_num)
        query = data.get("query") # If we're moving to a new page of results, use the same query
	
	#Search done here
    search_results_tuple = search("static/index", str(query), page_num)
    search_results = search_results_tuple[0]
    lengthList = len(search_results)

    return render_template(
        'PikaPediaHomepage.html',
        search_results=search_results,
        lengthList=lengthList,
        query=query,
        page_num=page_num,
        total_results=search_results_tuple[1]
    )

#lets you make changes and view in browser.
#Found at URL: http://flask.pocoo.org/snippets/40/
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
	app.run(debug=True)
