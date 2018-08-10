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

app = Flask(__name__)

@app.route("/testpage")
def birthdays():
    print("TestPage Triggered")
    dates = {"bulbasaur": 1, "ivysaur": 2, "venusaur": 3, "charmander": 4, "charmeleon": 5, "charizard": 6, "squirtle": 7, "wartortle": 8, "blastoise": 9}
    x = int(100)
    return render_template("testpage.html", dates=dates, x=x)

''' Old homepage
@app.route('/', methods=['GET', 'POST'])
def index():
	print("HomepageTriggered")
	return render_template('ProjectHomepage.html')
'''

@app.route('/', methods=['GET', 'POST'])
def PikaPediaHomepage():
    if request.method == 'POST':
        data = request.form
    else:
        data = request.args

    print("HomepageTriggered")
    #Works with this list
    #
    #  ToDo: change this into a new list of search results
    #
    TempSearchResults = ('bulbasaur', 'ivysaur','venusaur', 'charmander', 'charmeleon', 'charizard', 'squirtle', 'wartortle', 'blastoise')
    TempSearchResults2 = ('ivysaur','venusaur', 'charmander', 'charmeleon', 'charizard', 'squirtle', 'wartortle', 'blastoise')
    SearchTerm = "bulbasaur"


    query = data.get('IndexSearch')
    TempSearchResults = mainSearch(str(query))
    lengthList = len(TempSearchResults)

    print("Results: "+ str(TempSearchResults))
    #time.sleep(5)   # Delays for 5 seconds. You can also use a float value.
    #TempSearchResults = TempSearchResults2


    return render_template('PikaPediaHomepage.html', TempSearchResults=TempSearchResults, lengthList=lengthList)

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

###indexer
#
#
def search(indexer, search_term):
    results = None
    SearchResults = ()
    with indexer.searcher() as searcher:
        query = MultifieldParser(["title", "content"], schema=indexer.schema).parse(search_term)
        results = searcher.search(query)
        print("Number of results: " + str(len(results)))
        for result in results:
            SearchResults = SearchResults + (str(result['title']),)
    return SearchResults

'''Creates the index in the given directory'''
def index(db_name, index_dir):

    # This is the schema that will be followed by the documents in our index
    # We may or may not want to add some fields
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))
        # Make sure the directory where we will be putting the index exists
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        # Create the index inside of the directory
    indexer = create_in(index_dir, schema)
        # The writer is used to add documents to the index
    writer = indexer.writer()
        # Index each tuple in the csv file
    with open(db_name, 'r') as csv_file:
        csv_file = open(db_name, 'r')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            writer.add_document(title=row['Name'], path='/' + row['Number'], content=' '.join(list(row.values())))
        writer.commit()
    return indexer

def mainSearch(SearchTerm):
    indexer = index("static/Storage/PokeData.csv", "index_dir")
        # Makeshift temporary search interface
    #while (True):
        #search_term = input("Search: ")
    search_term = SearchTerm
    #if search_term == "quit":
    #    break
    SearchTerm = search(indexer, search_term)
    print("\n\nResults: "+str(SearchTerm))

    return SearchTerm

if __name__ == '__main__':
	app.run(debug=True)
