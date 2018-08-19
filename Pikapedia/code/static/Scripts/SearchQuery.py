'''Searches through the index using the given search phrase and prints the search results'''
def search(indexer, search_term):
    results = None
    with indexer.searcher() as searcher:
        query = MultifieldParser(["title", "content"], schema=indexer.schema).parse(search_term)
        results = searcher.search(query)
        print("Number of results: " + str(len(results)))
        for result in results:
            print(result['title'] + ": " + result['content'][:50] + "...") # Print the first 50 characters of the each result
        print("")

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
    import whoosh
    import os
    import csv
    from whoosh.index import create_in
    from whoosh.fields import *
    from whoosh.qparser import QueryParser
    from whoosh.qparser import MultifieldParser
    indexer = index("static/Storage/PokeData.csv", "index_dir")
        # Makeshift temporary search interface
    while (True):
        search_term = input("Search: ")
        search_term = Term
        if search_term == "quit":
            break
        search(indexer, search_term)
