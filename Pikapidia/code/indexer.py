import sys
import whoosh
import os
import csv
import json
import string
from whoosh.index import create_in, open_dir
from whoosh.fields import * 
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser

'''Searches through the index using the given search phrase.
    Returns a list containing the search results for the given page as well as the total number of results.'''
def search(index_dir, search_term, page_num):
    indexer = open_dir(index_dir)
    results = None

    # Remove any punctuation from the query (special treatment of ' for Farfetch'd)
    search_term = search_term.translate({ord(c): (' ' if c != "'" else '') for c in (string.punctuation)}) # From Blckknght on stack overflow
    print("Searching for \"" + search_term + "\"")

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
                "moves",
                "first_form",
                "second_forms",
                "third_forms"
            ],
            schema=indexer.schema, 
            group=qparser.OrGroup
        ).parse(search_term)

        results = searcher.search_page(query, page_num, pagelen=15) # Return the top 200 results matching the query
        num_results = len(results)
        print("Query matches: " + str(num_results))
        print("Results returned: " + str(results.scored_length()))

        # Results are inaccessible after the searcher closes, so make a copy
        results_list = []
        for result in results:
            result_dict = {}
            for key, value in result.items():
                if key in ['moves', 'second_forms', 'third_forms']:
                    value = value.split(' ')
                result_dict[key] = value
            results_list.append(result_dict)       

    return (results_list, num_results)

'''Creates the index in the given directory'''
def index(pokemon_db, evolutions_db, index_dir):
    # This is the schema that will be followed by the documents in our index
    schema = Schema(
        name=TEXT(stored=True), 
        id=ID(stored=True), 
        type_1=TEXT(stored=True),
        type_2=TEXT(stored=True),
        ability_1=TEXT(stored=True),
        ability_2=TEXT(stored=True),
        ability_hidden=TEXT(stored=True),
        moves=TEXT(stored=True),
        speed=STORED(), # STORED() means it won't be indexed and can't be searched for, but is still accessible
        sp_def=STORED(),
        sp_atk=STORED(),
        defense=STORED(),
        attack=STORED(),
        hp=STORED(),
        exp=STORED(),
        height=STORED(),
        weight=STORED(),
        first_form=TEXT(stored=True),
        second_forms=TEXT(stored=True),
        third_forms=TEXT(stored=True),
    )

    # Make sure the directory where we will be putting the index exists
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    # Create the index inside of the directory
    indexer = create_in(index_dir, schema)
    
    # The writer is used to add documents to the index
    writer = indexer.writer()

    # Index each tuple in the csv file
    with open(pokemon_db, 'r') as pokemon_csv:
        pokemon_csv_reader = csv.DictReader(pokemon_csv)
        for row in pokemon_csv_reader:
            evolution_line = ["", "", ""]
            # Find the Pokemon's evolution line
            with open(evolutions_db, 'r') as evolutions_csv:
                evolutions_csv_reader = csv.DictReader(evolutions_csv)
                for evolution_chain in evolutions_csv_reader:
                    if row['Name'] == evolution_chain['First Form'] or row['Name'] in evolution_chain['Second Forms'] or row['Name'] in evolution_chain['Third Forms']:
                        evolution_line[0] = evolution_chain['First Form']
                        evolution_line[1] = evolution_chain['Second Forms'].strip("[]").replace("'", "").replace(',', '')
                        evolution_line[2] = evolution_chain['Third Forms'].strip("[]").replace("'", "").replace(',', '')
                        break

            if row['Name'] == "glaceon" or row['Name'] == "leafeon":
                pass

            # Index the Pokemon's data
            writer.add_document(
                name=row['Name'], 
                id=row['Number'], 
                type_1=row["Type 1"],
                type_2=row["Type 2"],
                ability_1=row["Ability 1"],
                ability_2=row["Ability 2"],
                ability_hidden=row["Hidden Ability"],
                moves=row["Moves"].strip("[]").replace("'", "").replace(',', ''),
                speed=row["Speed"],
                sp_def=row["Special Defense"],
                sp_atk=row["Special Attack"],
                defense=row["Defense"],
                attack=row["Attack"],
                hp=row["HP"],
                exp=row["Base Experience"],
                height=row["Height"],
                weight=row["Weight"],
                first_form=evolution_line[0],
                second_forms=evolution_line[1],
                third_forms=evolution_line[2]
            )

    writer.commit()
    return indexer

def main():
    index_dir = "index_dir"
    indexer = index("PokeData.csv", "EvolutionChains.csv", index_dir)

    # Makeshift search interface for testing
    while (True):
        search_term = input("Search: ")
        if search_term == "quit":
            break
        search(index_dir, search_term, 1)

if __name__ == '__main__':
    main()