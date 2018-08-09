from lxml import html
import requests
import json

def main():

	f = open("PokeData.csv", "a+")

	urlTemplate = "http://pokeapi.co/api/v2/pokemon/"

	ListOfPokemonInfo = []

	for Pokemon in range(1,800):
		url = urlTemplate+str(Pokemon)
    		#print(url)
		page = requests.get(url)
		tree = html.fromstring(page.content)
		#print(page.content)
		newVar = json.loads(page.content.decode('utf-8'))
		Stats = []    #this will record stats
		StatsName = []    #this will record stats
		Name = newVar['name'] #this will return name
		BaseExperience = newVar['base_experience']     #returns experience gained for defeating this
		Height = newVar['height']

    		#print(newVar)

		for i in range(6):
			StatsName.append(newVar['stats'][i]['stat']['name'])
			Stats.append(newVar['stats'][i]['base_stat'])

		f.write('%s;' % str(Pokemon))
		f.write('%s;' % str(Name))
		f.write('%s;' % str(BaseExperience))
		f.write('%s;' % str(Height))

    		#print("Pokemon #"+str(Pokemon)+": ")
   		#print(" Name:   "+str(Name))
    		#print(" BaseExperience: "+str(BaseExperience))
    		#print(" Height  : "+str(Height))
    
		for i in range(6):
			f.write('%s;' % str(StatsName[i]))
			f.write('%s;' % str(Stats[i]))
        		#print(" Stat: "+str(StatsName[i])+" -----> "+str(Stats[i]))

		f.write("\n")

	f.close()




if __name__ == '__main__':
	main()
