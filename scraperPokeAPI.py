from lxml import html
import requests
import json
import csv

def main():

	f = open("PokeData.csv", "a+", newline='')

	csvwrite = csv.writer(f, delimiter = ',')

	urlTemplate = "http://pokeapi.co/api/v2/pokemon/"


	csvwrite.writerow(('Number','Name','Base Experience','Height','Type 1','Type 2','Ability 1','Ability 2','Ability 2','Stat 1','Stat 2','Stat 3','Stat 4','Stat 5','Stat 6'))

	ListOfPokemonInfo = []
	print("Before Scrape")
	for Pokemon in range(1,10):
		url = urlTemplate+str(Pokemon)
    		#print(url)
		page = requests.get(url)
		tree = html.fromstring(page.content)
		#print(page.content)
		newVar = json.loads(page.content.decode('utf-8'))
		Stats = []    #this will record stats
		TypeName = [] 	#this will record Types
		AbilityName = []	#this will record abilities
		StatsName = []    #this will record stats
		Name = newVar['name'] #this will return name
		BaseExperience = newVar['base_experience']     #returns experience gained for defeating this
		Height = newVar['height']
		#Ability = newVar['abilities'][3]['name']

		test_list = (str(Pokemon),str(Name),str(BaseExperience),str(Height),)
		
		for num in range(len(newVar['abilities'])):
			AbilityName.append(str(newVar['abilities'][num]['ability']['name']))
    		#print(newVar)

		for num in range(len(newVar['types'])):
			TypeName.append(str(newVar['types'][num]['type']['name']))
			
		for i in range(6):
			StatsName.append(newVar['stats'][i]['stat']['name'])
			Stats.append(newVar['stats'][i]['base_stat'])

		stat_list = []

		#Types to added to test_list here. I used 2 because this is most possible
		for num in range(len(TypeName)):
			test_list = test_list + (str(TypeName[num]),)
		for num in range(2-len(TypeName)):
			test_list = test_list + (("None"),)
		
		#Ability to added to test_list here. I used 3 because this is most possible
		for num in range(len(AbilityName)):
			test_list = test_list + (str(AbilityName[num]),)
		for num in range(3-len(AbilityName)):
			test_list = test_list + (("None"),)
		
		
		#Stats to added to test_list here.
		for i in range(6):
			stat_list.append(str(StatsName[i])+": "+str(Stats[i]))
			test_list = test_list + (str(stat_list[i]),)

		#print(stat_list)

		#test_list = []

		#','.join(str(stat_list))
		'''str(stat_list[0])
		 ,str(stat_list[1]),str(stat_list[2])
		  ,str(stat_list[3]),str(stat_list[4])
		   ,str(stat_list[5]))
		'''
		#Additions to the csv will go here

		print(test_list)
		csvwrite.writerow(test_list)

		#csvwrite.writerow(stat_list)

		#f.write('%s;' % str(Pokemon))
		#f.write('%s;' % str(Name))
		#f.write('%s;' % str(BaseExperience))
		#f.write('%s;' % str(Height))

    		#print("Pokemon #"+str(Pokemon)+": ")
   		#print(" Name:   "+str(Name))
    		#print(" BaseExperience: "+str(BaseExperience))
    		#print(" Height  : "+str(Height))

		#for i in range(6):
			#f.write('%s;' % str(StatsName[i]))
			#f.write('%s;' % str(Stats[i]))
        		#print(" Stat: "+str(StatsName[i])+" -----> "+str(Stats[i]))

		#f.write("\n")

	f.close()




if __name__ == '__main__':
	main()
