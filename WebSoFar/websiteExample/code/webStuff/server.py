from flask import Flask, render_template, url_for, request
import os
import time
import sys
import whoosh
import os
import csv
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
    print("\n\nResults: "+str(search_results))
    lengthList = len(search_results)

    print("Results: "+ str(search_results))
    #time.sleep(5)   # Delays for 5 seconds. You can also use a float value.

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
