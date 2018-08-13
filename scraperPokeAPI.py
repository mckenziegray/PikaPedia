from lxml import html
import requests
import json
import csv

def main():
	NUM_POKEMON_TO_SCRAPE = 802 # Total 802
	urlTemplate = "http://pokeapi.co/api/v2/pokemon/"

	with open("PokeData.csv", "w") as f: # 'with' provides free exception handling and closes the file automatically
		csvwriter = csv.writer(f, delimiter = ',')
		csvwriter.writerow(('Number','Name','Base Experience','Height', 'Weight', 'Type 1','Type 2','Ability 1','Ability 2','Ability 3','Speed','Special Defense','Special Attack','Defense','Attack','HP'))

		# print("Before Scrape")
		for Pokemon in range(1, NUM_POKEMON_TO_SCRAPE):
			url = urlTemplate+str(Pokemon)
			page = requests.get(url)
			json_data = json.loads(page.content.decode('utf-8'))
			Stats = []    #this will record stats
			Types = [] 	#this will record Types
			Abilities = []	#this will record abilities
			Moves = [] #records the pokemon's moves
			Name = json_data['name'] #this will return name
			BaseExperience = json_data['base_experience']     #returns experience gained for defeating this
			Height = json_data['height']
			Weight = json_data['weight']
			#Ability = json_data['abilities'][3]['name']

			test_list = (str(Pokemon),str(Name),str(BaseExperience),str(Height),str(Weight),)

			for num in range(len(json_data['abilities'])):
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
			for num in range(3-len(Abilities)):
				test_list = test_list + (("None"),)
				
			stat_list = []
		
			#Stats to added to test_list here.
			for i in range(6):
				stat_list.append(str(Stats[i]))
				test_list = test_list + (str(stat_list[i]),)

			test_list += (str(Moves),)

			print(test_list)
			csvwriter.writerow(test_list)

if __name__ == '__main__':
	main()
