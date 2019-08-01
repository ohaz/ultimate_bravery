import copy

from flask import Flask, render_template, redirect, url_for
import json
import os
import base64
import random


app = Flask(__name__)

map_name_translator = {
    "SR": "Summoners Rift",
    "HA": "Howling Abyss",
    "TT": "Twisted Treeline",
    "CS": "Crystal Scar"
}

data = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('impressum.html')


@app.route('/reload/')
def reload():
    global data
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'items.json')) as json_file:
        data = json.loads(json_file.read())
    return redirect(url_for('index'))


@app.route('/g/<game_map>/')
def generate(game_map):
    if game_map not in map_name_translator:
        return 404
    valid_summoners = [x for x in data['summoners'] if game_map in x['modes']]
    random.shuffle(valid_summoners)
    valid_boots = [x for x in data['boots'] if game_map in x['modes']]
    valid_items = [x for x in data['items'] if game_map in x['modes']]
    random.shuffle(valid_items)
    random.shuffle(valid_boots)
    summoner_spells = [
        {
            "name": valid_summoners[0]['name'],
            "icon": valid_summoners[0]['image_path'],
        },
        {
            "name": valid_summoners[1]['name'],
            "icon": valid_summoners[1]['image_path'],
        }
    ]
    max_first = ["Q", "W", "E"]
    random.shuffle(max_first)
    max_first = max_first[0]
    items = [
        {
            "name": valid_boots[0]['name'],
            "icon": valid_boots[0]['image_path'],
        }
    ]
    for i in range(5):
        items.append(
            {
                'name': valid_items[i]['name'],
                'icon': valid_items[i]['image_path']
            }
        )

    # Generate URL
    url = url_for('show_code', game_map=game_map, code='')
    return render_template("showitems.html", items=items, max_first=max_first, summoner_spells=summoner_spells,
                           mapname=map_name_translator[game_map], game_map=game_map, url=url)


@app.route('/s/<game_map>/<code>')
def show_code(game_map, code):
    # Decode code:
    try:
        decoded = base64.b64decode(code.encode('ascii')).decode('ascii')
        splits = decoded.split('|')
        max_first = splits[0]
        temp_summoner_spells = splits[1].split(',')
        summoner_spells = [
            {
                "name": x['name'],
                "icon": 'gfx/summoners/' + x['icon'],
                "id": x['id']
            }
            for x in data['summoners'] if str(x['id']) in temp_summoner_spells
        ]
        temp_items = splits[2].split(',')
        boot = temp_items[0]
        temp_items = temp_items[1:]
        items = []
        for item in temp_items:
            current_data = data['items']
            if int(item) >= 9000:
                current_data = data['jungle']
            for x in current_data:
                if str(x['id']) == item:
                    items.append({
                        "name": x['name'],
                        "icon": 'gfx/items/' + x['icon'],
                        "id": x['id']
                    })
        for valid_boot in data['boots']:
            if boot == str(valid_boot['id']):
                boot = {
                    "name": valid_boot['name'],
                    "icon": 'gfx/items/boots/'+valid_boot['icon'],
                    "id": valid_boot['id']
                }
                break
        items.insert(0, boot)
        for valid_enchantment in data['boots_enchantments']:
            if splits[3] == str(valid_enchantment['id']):
                boot_enchantment = {
                    "name": valid_enchantment['name'],
                    "icon": 'gfx/items/boots/'+valid_enchantment['icon'],
                    "id": valid_enchantment['id']
                }
                break
        return render_template("showitems.html", items=items, max_first=max_first, boot_enchantment=boot_enchantment,
                               summoner_spells=summoner_spells, mapname=map_name_translator[game_map],
                               url=url_for('show_code', game_map=game_map, code=code), game_map=game_map)
    except Exception as e:
        return "ERROR"
    return 200


if __name__ == '__main__':

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'items.json')) as json_file:
        data = json.loads(json_file.read())

    app.run(host='127.0.0.1', port=51114)
