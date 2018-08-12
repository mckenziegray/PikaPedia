from lxml import html
import requests
import json
import csv

pokemon_base_url = "http://pokeapi.co/api/v2/pokemon/"
evolutions_base_url = "http://pokeapi.co/api/v2/evolution-chain/"

def scrape_pokemon(file_name, start_id, end_id):
	with open(file_name, "w", newline='') as f: # 'with' provides free exception handling and closes the file automatically
		csvwriter = csv.writer(f, delimiter = ',')
		csvwriter.writerow(('Number','Name','Base Experience','Height','Type 1','Type 2','Ability 1','Ability 2','Ability 3','Speed','Special Defense','Special Attack','Defense','Attack','HP'))

		# print("Before Scrape")
		for pokemon_id in range(start_id, end_id+1):
			url = pokemon_base_url+str(pokemon_id)
			page = requests.get(url)
			json_data = json.loads(page.content.decode('utf-8'))
			Stats = []    #this will record stats
			Types = [] 	#this will record Types
			Abilities = []	#this will record abilities
			Name = json_data['name'] #this will return name
			BaseExperience = json_data['base_experience']     #returns experience gained for defeating this
			Height = json_data['height']
			#Ability = json_data['abilities'][3]['name']

			test_list = (str(pokemon_id),str(Name),str(BaseExperience),str(Height),)

			for num in range(len(json_data['abilities'])):
				Abilities.append(str(json_data['abilities'][num]['ability']['name']))

			for num in range(len(json_data['types'])):
				Types.append(str(json_data['types'][num]['type']['name']))

			for i in range(6):
				Stats.append(json_data['stats'][i]['base_stat'])

			#Types to added to test_list here. I used 2 because this is most possible
			for num in range(len(Types)):
				test_list = test_list + (str(Types[num]),)
			for num in range(2-len(Types)):
				test_list = test_list + (("None"),)
		
			#Ability to added to test_list here. I used 3 because this is most possible
			for num in range(len(Abilities)):
				test_list = test_list + (str(Abilities[num]),)
			for num in range(3-len(Abilities)):
				test_list = test_list + (("None"),)
				
			stat_list = []
		
			#Stats to added to test_list here.
			for i in range(6):
				stat_list.append(str(Stats[i]))
				test_list = test_list + (str(stat_list[i]),)

			print(test_list)
			csvwriter.writerow(test_list)

def scrape_evolutions(file_name, start_id, end_id):
	with open(file_name, "w", newline='') as f:
		csvwriter = csv.writer(f, delimiter = ',')
		csvwriter.writerow(('id','First Form','Second Forms','Third Forms'))

		for chain_id in range(start_id, end_id+1):
			if chain_id == 210: # For some reaoson, the API skips 210
				continue
			url = evolutions_base_url+str(chain_id)
			page = requests.get(url)
			json_data = json.loads(page.content.decode('utf-8'))

			first_form = json_data['chain']['species']['name']

			second_forms = []
			for evolution in json_data['chain']['evolves_to']:
				second_forms.append(evolution['species']['name'])

			third_forms = []
			if len(second_forms) > 0:
				for evolution in json_data['chain']['evolves_to'][0]['evolves_to']:
					third_forms.append(evolution['species']['name'])

			row = (chain_id, first_form, second_forms, third_forms)
			print(row)
			csvwriter.writerow(row)

def main():
	scrape_evolutions("EvolutionChains.csv", 1, 423) # Total 423
	scrape_pokemon("PokeData1.csv", 1, 802) # Total 802

if __name__ == '__main__':
	main()
