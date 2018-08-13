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
                "evolution_line"
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
        speed=STORED(), # Stored means it won't be indexed and can't be searched for, but is still accessible
        sp_def=STORED(),
        sp_atk=STORED(),
        defense=STORED(),
        attack=STORED(),
        hp=STORED(),
        exp=STORED(),
        height=STORED(),
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
                        evolution_line =
                            [
                                evolution_chain['First Form'], 
                                evolution_chain['Second Forms'].strip("[']").replace(',', ' '), 
                                evolution_chain['Third Forms'].strip("[']").replace(',', ' ')
                            ]
                        )
                        break

            # Index the Pokemon's data
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
                height=row["Height"],
                first_form=evolution_line[0],
                second_forms=evolution_line[1],
                third_forms=evolution_line[2]
            )

    writer.commit()
    return indexer

def main():
    indexer = index("PokeData.csv", "EvolutionChains.csv", "index_dir")

    # Makeshift search interface for testing
    while (True):
        search_term = input("Search: ")
        if search_term == "quit":
            break
        search(indexer, search_term)

if __name__ == '__main__':
    main()