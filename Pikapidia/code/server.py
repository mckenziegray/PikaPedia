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

sys.path.append("../../../..") # Any imports below this will come from the PikaPedia directory
from indexer import *

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

	#Stores variables that will later be passed into the page
    name = info['name']
    id = info['id']
    idInt = int(id)
    type_1 = info['type_2']
    type_2 = info['type_1']
    ability_1 = info['ability_1']
    ability_2 = info['ability_2']
    moves = info['moves']
    first_form = info['first_form']
    second_forms = info['second_forms']
    third_forms = info['third_forms']
    pokemonEvo2Length = len(second_forms)
    pokemonEvo3Length = len(third_forms)

    return render_template('SinglePokemonLoadPage.html',
    #Variables for web page
        name=name,
        id=id,
        type_1=type_1,
        type_2=type_2,
        hp = info['hp'],
        attack = info['attack'],
        defense = info['defense'],
        sp_atk = info['sp_atk'],
        sp_def = info['sp_def'],
        speed = info['speed'],
        height = int(info['height']),
        weight = int(info['weight']),
        ability_1=ability_1,
        ability_2=ability_2,
        hidden_ability=info['ability_hidden'],
        moves=moves,
        first_form=first_form,
        second_forms=second_forms,
        third_forms=third_forms,
        idInt=idInt,    #used for Counter in HTML
        moveList=moves, #Holds Moves List
        pokemonEvo2Length=pokemonEvo2Length,
        pokemonEvo3Length=pokemonEvo3Length)

#Loads Search Page for pokemon
#		
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
        query = data.get('IndexSearch')
    else:
        page_num = int(page_num)
        query = data.get("query") # If we're moving to a new page of results, use the same query
	
	#Search done here
    search_results_tuple = search("index_dir", str(query), page_num)
    search_results = search_results_tuple[0]
    lengthList = len(search_results)
    #print("Total results: " + str(search_results_tuple[1]))

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
