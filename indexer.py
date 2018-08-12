import sys
import whoosh
import os
import csv
from whoosh.index import create_in
from whoosh.fields import * 
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser

'''Searches through the index using the given search phrase and prints the search results'''
def search(indexer, search_term):
    results = None
    with indexer.searcher() as searcher:
        query = MultifieldParser(
            [
                "name", 
                "id",
                "type_1",
                "type_2",
                "ability_1",
                "ability_2",
                "ability_hidden",
            ],
            schema=indexer.schema, 
            group=qparser.OrGroup
        ).parse(search_term)
        results = searcher.search(query, limit=200) # Return the top 200 results matching the query
        print("Query matches: " + str(len(results)))
        print("Results returned: " + str(results.scored_length()))

        # Results are inaccessible after the searcher closes, so make a copy
        results_list = []
        for result in results:
            result_dict = {}
            for key, value in result.items():
                result_dict[key] = value
            results_list.append(result_dict)

    return results_list

'''Creates the index in the given directory'''
def index(db_name, index_dir):
    # This is the schema that will be followed by the documents in our index
    schema = Schema(
        name=TEXT(stored=True), 
        id=ID(stored=True), 
        type_1=TEXT(stored=True),
        type_2=TEXT(stored=True),
        ability_1=TEXT(stored=True),
        ability_2=TEXT(stored=True),
        ability_hidden=TEXT(stored=True),
        speed=STORED(), # Stored means it won't be indexed and can't be searched for, but is still accessible
        sp_def=STORED(),
        sp_atk=STORED(),
        defense=STORED(),
        attack=STORED(),
        hp=STORED(),
        exp=STORED(),
        height=STORED()
    )

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
            writer.add_document(
                name=row['Name'], 
                id=row['Number'], 
                type_1=row["Type 1"],
                type_2=row["Type 2"],
                ability_1=row["Ability 1"],
                ability_2=row["Ability 2"],
                ability_hidden=row["Ability 2"],
                speed=row["Speed"],
                sp_def=row["Special Defense"],
                sp_atk=row["Special Attack"],
                defense=row["Defense"],
                attack=row["Attack"],
                hp=row["HP"],
                exp=row["Base Experience"],
                height=row["Height"]
            )

    writer.commit()
    return indexer

def main():
    indexer = index("PokeData.csv", "index_dir")

    # Makeshift search interface for testing
    while (True):
        search_term = input("Search: ")
        if search_term == "quit":
            break
        search(indexer, search_term)

if __name__ == '__main__':
    main()