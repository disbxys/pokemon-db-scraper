from bs4 import BeautifulSoup
from datetime import datetime
import json

import requests

from pokemon import Pokemon

URL = "https://pokemondb.net/pokedex/all"

def main() -> None:
    
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.content, "html.parser")

    # a list to contain all the data about pokemon
    pokedex = list()

    # filter only the elements in the pokedex table
    # containg information about pokemon
    for elem in soup.select('table[id="pokedex"] > tbody > tr'):
        pokedex_entry = Pokemon(elem)

        pokedex.append(pokedex_entry.gather())
        # print(pokedex_entry.id + " \t|\t " + pokedex_entry.name)

    # dump to file
    write_to_file(container=pokedex, pretty_print=True, record_date=True)


def write_to_file(filename:str="pokedex", container=[], 
                record_date:bool=False, pretty_print:bool=False) -> None:
    if record_date:
        # append the current date the filename
        filename += ' ' + str(datetime.today().date()) + ".json"
    else:
        filename += ".json"

    if pretty_print:
        with open(filename, 'w+', encoding='utf-8') as outfile:
            outfile.write(json.dumps(container, indent=4))
    else:
        with open(filename, 'w+', encoding='utf-8') as outfile:
            outfile.write(json.dumps(container))

if __name__ == '__main__':
    main()