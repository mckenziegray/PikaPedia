from lxml import html
import requests

page = requests.get('https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number')
tree = html.fromstring(page.content)

#print(page.content)
pokemonList = []

linebyline = []
line = []
for num in range(len(page.content)):
    if(page.content[num]!='\n'):
        line.append(page.content[num])
        #print(page.content[num]):
    else:
        linebyline.append(''.join(line))
        line = []

for num in range(len(linebyline)):
    if ("<td>" in linebyline[num] or "<tr>" in linebyline[num]):
        #print(linebyline[num])
        while ("</td>" not in linebyline[num] or "</tr>" not in linebyline[num]):
            if ("_(Pok%C3%A9mon)" in linebyline[num] and "src" in linebyline[num]):
                p = 20
                while linebyline[num][p]!='_':
                    #print(linebyline[num])
                    #lines = linebyline[num][20:p+1]
                    #B = [str(x) for x in linebyline[num].split(',') if x.strip()]
                    #print(lines)
                    p += 1
                lines = linebyline[num][20:p]
                pokemonList.append(lines)
                #print(lines)
            num += 1

filetype = open('test.txt', 'w')
for pokemon in pokemonList:
    pokeurl = "https://bulbapedia.bulbagarden.net/wiki/"+str(pokemon)
    print(pokeurl)
    page = requests.get("https://bulbapedia.bulbagarden.net/wiki/"+str(pokemon))
    #for num in range(len(page.content)):
    print("HERE")
    #input()
    linebyline = []
    line = []
    for num in range(len(page.content)):
        if(page.content[num]!='\n'):
            line.append(page.content[num])
            #print(page.content[num])
        else:
            linebyline.append(''.join(line))
            line = []

    for num in range(len(linebyline)):
        filetype.write(linebyline[num])
        if ("style=\"color:#000" in linebyline[num]):
            print(linebyline[num])
        #    while ("</tbody>" not in linebyline[num]):
        #        print(linebyline[num])
        #        num += 1

    exit()

#(Pok%C3%A9mon
