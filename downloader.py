
import requests
from bs4 import BeautifulSoup
from time import sleep, time
import random
import shutil
from os import path
import re
import pprint
import json
from urllib.parse import unquote
from tqdm import tqdm

ROOT_DIR = path.dirname(path.realpath(__file__))
pp = pprint.PrettyPrinter(indent=4)

filters = [
    'ornn,forge',
    ',Gangplank'
]

boot_filter = [
    'Berserker\'s Greaves',
    'Boots of Mobility',
    'Boots of Swiftness',
    'Ghostwalkers',
    'Ionian Boots of Lucidity',
    'Mercury\'s Treads',
    'Ninja Tabi',
    'Sorcerer\'s Shoes'
]


def name_to_filename(name):
    return name.replace(' ', '_')


def download_image(url, name):
    image_response = requests.get(url, stream=True)
    save_path = path.join(ROOT_DIR, 'static', 'items', name_to_filename(name) + '.png')
    if image_response.status_code == 200:
        with open(save_path, 'wb') as skill_image:
            shutil.copyfileobj(image_response.raw, skill_image)
    return save_path


def save_json(boots, items, summoners):
    items_dct = {'boots': boots, 'items': items, 'summoners': summoners}
    skill_path = path.join(ROOT_DIR, 'items.json')
    with open(skill_path, 'w') as outfile:
        json.dump(items_dct, outfile, indent=4)


def get_items(base_path):
    list_of_items = requests.get(base_path + 'wiki/Item')
    if list_of_items.status_code == 200:
        items = list_of_items.text[
                list_of_items.text.index('<dt>Finished items'):list_of_items.text.index('<dt>Removed items')]
        html = BeautifulSoup(items, 'html.parser')
        content = html.find('div', {'class': 'tlist'})
        items = []
        boots = []
        for item in content.find_all('div', {'class': 'item-icon'}):
            skip = False
            for filter in filters:
                if filter in item['data-search']:
                    skip = True
            if skip:
                continue
            image_div = item.find('img', {'class': 'thumbborder'})
            new_item = {'name': item['data-param'], 'modes': item['data-modes'],
                        'image_path': image_div['data-src']}
            if new_item['name'] in boot_filter:
                boots.append(new_item)
            else:
                items.append(new_item)

        for boot in tqdm(boots):
            download_image(boot['image_path'], boot['name'])
            local_file_name = name_to_filename(boot['name'])
            boot['image_path'] = path.join(f'items/{local_file_name}.png')
            maps = boot['modes']
            boot['modes'] = []
            if 'ARAM' in maps:
                boot['modes'].append('HA')
            if 'Classic 5v5' in maps:
                boot['modes'].append('SR')
            if 'Classic 3v3' in maps:
                boot['modes'].append('TT')

        for item in tqdm(items):
            download_image(item['image_path'], item['name'])
            local_file_name = name_to_filename(item['name'])
            item['image_path'] = path.join(f'items/{local_file_name}.png')
            maps = item['modes']
            item['modes'] = []
            if 'ARAM' in maps:
                item['modes'].append('HA')
            if 'Classic 5v5' in maps:
                item['modes'].append('SR')
            if 'Classic 3v3' in maps:
                item['modes'].append('TT')
        return boots, items


def get_summoners(base_path):
    availables = {
        'Heal': ['SR', 'HA', 'TT'],
        'Ghost': ['SR', 'HA', 'TT'],
        'Barrier': ['SR', 'HA', 'TT'],
        'Exhaust': ['SR', 'HA', 'TT'],
        'Mark': ['HA'],
        'Clarity': ['HA'],
        'Flash': ['SR', 'HA', 'TT'],
        'Teleport': ['SR', 'TT'],
        'Smite': ['SR', 'TT'],
        'Cleanse': ['SR', 'HA', 'TT'],
        'Ignite': ['SR', 'HA', 'TT']
    }
    list_of_summoners = requests.get(base_path + 'wiki/Summoner_spell')
    if list_of_summoners.status_code == 200:
        html = BeautifulSoup(list_of_summoners.text, 'html.parser')
        table = html.find('table', {'class': 'article-table'})
        summoners = []
        for spell in table.find_all('div', {'class': 'spell-icon'}):
            name = spell['data-param']
            image_div = spell.find('img', {'alt': name})
            modes = availables.get(name, None)
            if modes:
                new_spell = {
                                'name': name, 'modes': modes,
                                'image_path': image_div['data-src']
                            }
                summoners.append(new_spell)
        for summoner in tqdm(summoners):
            download_image(summoner['image_path'], summoner['name'])
            local_file_name = name_to_filename(summoner['name'])
            summoner['image_path'] = path.join(f'items/{local_file_name}.png')
        return summoners


def main():
    BASE_PATH = 'https://leagueoflegends.fandom.com/'
    overwrite = False
    random.seed(time())

    boots, items = get_items(BASE_PATH)
    summoners = get_summoners(BASE_PATH)

    save_json(boots, items, summoners)


if __name__ == '__main__':
    main()

