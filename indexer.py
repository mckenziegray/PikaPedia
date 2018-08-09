import sys
import whoosh
import os
import csv
from whoosh.index import create_in
from whoosh.fields import * 
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser

'''Searches through the index using the given search phrase and prints the search results'''
def search(indexer, searchTerm):
    results = None
    with indexer.searcher() as searcher:
        query = MultifieldParser(["title", "content"], schema=indexer.schema).parse(searchTerm)
        results = searcher.search(query)
        print("Number of results: " + str(len(results)))
        for result in results:
            print(result['title'] + ": " + result['content'][:50] + "...") # Print the first 50 characters of the each result

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
    with open(db_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        header = True
        for row in csv_reader:
            if not header:
                writer.add_document(title=row['name'], path='/' + row['id'], content=' '.join(row))
            else:
                header = False

    writer.commit()
    return indexer

def main():
    searchTerm = 'bulbasaur'
    indexer = index("Pokedata.csv", "index_dir")
    search(indexer, searchTerm)

if __name__ == '__main__':
    main()