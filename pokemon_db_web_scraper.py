import bs4.element
from bs4 import BeautifulSoup
from collections import namedtuple
from datetime import datetime
import json

import requests

URL = "https://pokemondb.net/pokedex/all"

def run() -> None:
    
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.content, "html.parser")

    # a list to contain all the data about pokemon
    pokedex = list()

    # filter only the elements in the pokedex table
    # containg information about pokemon
    for elem in soup.select('table[id="pokedex"] > tbody > tr'):
        # get the pokedex id
        uid = get_id(elem)

        # get the name registered in the pokedex
        name = get_name(elem)

        # get the type(s)
        types = get_types(elem)

        # get the total stat value and individual
        # stat values
        # stats are assumed to be in the order:
        #   - total, hp, atk, def, sp atk, sp def, spd
        # For now, it would be safe to assume that each
        # tag would be stored in propoer order. At the
        # time of writing this, there is no way to
        # definitely determine if list is in proper order.
        stats = get_stats(elem)

        pokedex_entry = {
            "id": uid,
            "name": name,
            "type": types,
            "stats": stats
        }

        pokedex.append(pokedex_entry)

        print(pokedex_entry['id'])

    # dump to file
    write_to_file(container=pokedex, pretty_print=True)


def get_id(tag:bs4.element.Tag) -> str:
    elem = tag.select_one('[class="infocard-cell-data"]')
    if elem: return int(elem.text)
    else: None


def get_name(tag:bs4.element.Tag) -> str:
    elem = tag.select_one('[class="ent-name"]')
    if elem:
        name = elem.text
        sub_name = tag.select_one('small[class="text-muted"]')

        if sub_name:
            name += ' ' + sub_name.text

        return name

    else:
        return None


def get_types(tag:bs4.element.Tag) -> list:
    # look for tags containing the name of a type
    return [elem.text for elem in tag.select('[class^="type-icon"]')]


def get_stats(tag:bs4.element.Tag) -> list:
    # The total stats value is located in a tag
    # with a class different from the tags
    # containing the individual stat values.
    total_stats_value_tag = tag.select_one('td[class="cell-total"]')
    total_stats_value = None    # default value
    if total_stats_value_tag:
        total_stats_value = total_stats_value_tag.text

    individual_stats = list()
    for individual_stats_tag in tag.select('td[class="cell-num"]'):
        individual_stats.append(individual_stats_tag.text)

    return [total_stats_value] + individual_stats


def write_to_file(filename:str="pokedex",
                container=[],
                record_date:bool=False,
                pretty_print:bool=False) -> None:
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
    run()