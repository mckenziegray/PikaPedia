from lxml import html
import requests
import json

urlTemplate = "http://pokeapi.co/api/v2/pokemon/"

ListOfPokemonInfo = []

for Pokemon in range(1,800):
    url = urlTemplate+str(Pokemon)
    #print(url)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    #print(page.content)
    newVar = json.loads(page.content)
    
    Stats = []    #this will record stats
    StatsName = []    #this will record stats
    Name = newVar['name'] #this will return name
    BaseExperience = newVar['base_experience']     #returns experience gained for defeating this
    Height = newVar['height']

    #print(newVar)
    for i in range(6):
        #print(newVar['stats'][i]['stat']['name'])
        #print(newVar['stats'][i]['base_stat'])
        StatsName.append(newVar['stats'][i]['stat']['name'])
        Stats.append(newVar['stats'][i]['base_stat'])

    ###################################################

    print("Pokemon #"+str(Pokemon)+": ")
    print(" Name:   "+str(Name))
    print(" BaseExperience: "+str(BaseExperience))
    print(" Height  : "+str(Height))
    for i in range(6):
        print(" Stat: "+str(StatsName[i])+" -----> "+str(Stats[i]))
