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

@app.route("/testpage")
def birthdays():
    print("TestPage Triggered")
    dates = {"bulbasaur": 1, "ivysaur": 2, "venusaur": 3, "charmander": 4, "charmeleon": 5, "charizard": 6, "squirtle": 7, "wartortle": 8, "blastoise": 9}
    x = int(100)
    return render_template("testpage.html", dates=dates, x=x)


@app.route('/SinglePokemonLoadPage', methods=['GET', 'POST', 'pokemonInfo'])
def SinglePokemonLoadPage():
    if request.method == 'POST':
        data = request.form
    else:
        data = request.args

    print("Single Page Triggered")

    info = data.get('pokemonInfo')

    print(info.replace("'", '"'))
    lengthInfo = len(info)

    info = json.loads(info.replace("'", '"'))

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

    print()
    print(third_forms)
    print()

    return render_template('SinglePokemonLoadPage.html',
    #Variables for web page
        name=name,
        id=id,
        ability_1=ability_1,
        ability_2=ability_2,
        moves=moves,
        first_form=first_form,
        second_forms=second_forms,
        third_forms=third_forms,
        idInt=idInt,    #used for Counter in HTML
        moveList=moves, #Holds Moves List
        pokemonEvo2Length=pokemonEvo2Length,
        pokemonEvo3Length=pokemonEvo3Length)

@app.route('/', methods=['GET', 'POST'])
def PikaPediaHomepage():
    if request.method == 'POST':
        data = request.form
    else:
        data = request.args

    print("Homepage Triggered")
    indexer = index("static/Storage/PokeData.csv", "static/Storage/EvolutionChains.csv", "index_dir")
    query = data.get('IndexSearch')

    search_results = search(indexer, str(query))
    lengthList = len(search_results)

    return render_template('PikaPediaHomepage.html', search_results=search_results, lengthList=lengthList)

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
