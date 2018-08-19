import time
import urllib.request


#Images Scraped From URL: sprites.pokecheck.org
#
#   Example:
#       Bulbasaur:  https://sprites.pokecheck.org/i/001.gif
#       Ivysaur:    https://sprites.pokecheck.org/i/002.gif
#

import csv

def read_cell(x, y):
    count = 0
    with open('../Storage/PokeData.csv', 'r') as f:
        reader = csv.reader(f)
        for n in reader:
            if(n=="Name"):
                print("Saving Names: ")
                count -= 1
            else:
                if(count==650):
                    break
                else:
                    lenCount = len(str(count))
                    if(lenCount<=3):
                        tup = str(count)
                        for num in range(0,3-lenCount):
                            tup = "0" + tup
                        words = []
                        words.append(tup)
                    URL = str("https://sprites.pokecheck.org/i/"+str(tup)+".gif")
                    Image = str("../images/"+str(n[x])+".jpg")
                    print(URL, Image)
                    if(count!=0):
                        urllib.request.urlretrieve(URL, Image)
                    #time.sleep(1)
                    count += 1


print (read_cell(1, 802))
