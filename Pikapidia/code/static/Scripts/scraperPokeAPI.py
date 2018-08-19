from lxml import html
import requests
import json
import csv

pokemon_base_url = "http://pokeapi.co/api/v2/pokemon/"
evolutions_base_url = "http://pokeapi.co/api/v2/evolution-chain/"

'''Retrieves Pokemon data from the API and stores it in the given file in csv format'''
def scrape_pokemon(file_name, start_id, end_id):
	with open(file_name, "w", newline='') as f: # 'with' provides free exception handling and closes the file automatically
		csvwriter = csv.writer(f, delimiter = ',')
		csvwriter.writerow(('Number','Name','Base Experience','Height', 'Weight', 'Type 1','Type 2','Ability 1','Ability 2','Hidden Ability','Speed','Special Defense','Special Attack','Defense','Attack','HP', 'Moves'))

		# print("Before Scrape")
		for pokemon_id in range(start_id, end_id+1):
			url = pokemon_base_url+str(pokemon_id)
			page = requests.get(url)
			json_data = json.loads(page.content.decode('utf-8'))
			Stats = []    #this will record stats
			Types = [] 	#this will record Types
			Abilities = []	#this will record abilities
			HiddenAbility = None
			Moves = [] #records the pokemon's moves
			Name = json_data['name'] #this will return name
			BaseExperience = json_data['base_experience']     #returns experience gained for defeating this
			Height = json_data['height']
			Weight = json_data['weight']

			test_list = (str(pokemon_id),str(Name),str(BaseExperience),str(Height),str(Weight),)

			for num in range(len(json_data['abilities'])):
				if json_data['abilities'][num]['is_hidden']:
					HiddenAbility = json_data['abilities'][num]['ability']['name']
				else:
					Abilities.append(str(json_data['abilities'][num]['ability']['name']))

			for num in range(len(json_data['types'])):
				Types.append(str(json_data['types'][num]['type']['name']))

			for i in range(6):
				Stats.append(json_data['stats'][i]['base_stat'])
			
			for x in range(len(json_data['moves'])):
				Moves.append(str(json_data['moves'][x]['move']['name']))

			#Types to added to test_list here. I used 2 because this is most possible
			for num in range(len(Types)):
				test_list = test_list + (str(Types[num]),)
			for num in range(2-len(Types)):
				test_list = test_list + (("None"),)
		
			#Ability to added to test_list here. I used 3 because this is most possible
			for num in range(len(Abilities)):
				test_list = test_list + (str(Abilities[num]),)
			for num in range(2-len(Abilities)):
				test_list = test_list + (("None"),)
			
			test_list += ((str(HiddenAbility)),)
				
			stat_list = []
		
			#Stats to added to test_list here.
			for i in range(6):
				stat_list.append(str(Stats[i]))
				test_list = test_list + (str(stat_list[i]),)

			test_list += (str(Moves),)

			print(test_list)
			csvwriter.writerow(test_list)

'''Retrieves evolution data from the API and stores it in the given file in csv format'''
def scrape_evolutions(file_name, start_id, end_id):
	with open(file_name, "w", newline='') as f:
		csvwriter = csv.writer(f, delimiter = ',')
		csvwriter.writerow(('id','First Form','Second Forms','Third Forms'))

		for chain_id in range(start_id, end_id+1):
			
			url = evolutions_base_url+str(chain_id)
			page = requests.get(url)
			json_data = json.loads(page.content.decode('utf-8'))

			# Some of the evolution chains are just absent for some reason; skip them
			if not "chain" in json_data:
				continue
			
			# The base form of the evolutionary line
			first_form = json_data['chain']['species']['name']

			# A list of all second forms of the evolutionary line, if any exist
			second_forms = []
			for evolution in json_data['chain']['evolves_to']:
				second_forms.append(evolution['species']['name'])

			# A list of all third forms of the evolutionary line, if any exist
			third_forms = []
			if len(second_forms) > 0:
				for evolution in json_data['chain']['evolves_to'][0]['evolves_to']:
					third_forms.append(evolution['species']['name'])

			row = (chain_id, first_form, second_forms, third_forms)
			print(row)
			csvwriter.writerow(row)

def main():
	scrape_evolutions("EvolutionChains.csv", 1, 423) # Total 423
	scrape_pokemon("PokeData.csv", 1, 802) # Total 802

if __name__ == '__main__':
	main()
