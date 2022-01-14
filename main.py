import requests
import json
import os
import time

script_path = os.path.dirname(os.path.realpath(__file__))

if not os.path.isdir(os.path.join(script_path, 'datafiles')):
    os.mkdir(os.path.join(script_path, 'datafiles'))

bazaar = json.loads(requests.get("https://api.hypixel.net/skyblock/bazaar").text)
quick_stat = {}
quick_stat["last_update"] = time.time()

for item in bazaar["products"]:
    path = os.path.join(script_path, 'datafiles', item + '.json')
    quick_stat[item] = {}

    if not os.path.isfile(path):
        with open(path, 'w') as f:
            f.write("{}")
    with open(path, 'r') as f:
        item_data = json.load(f)
    
    if not("name" in item_data):
        item_data["name"] = item
    if not("history" in item_data):
        item_data["history"] = []

    if len(item_data["history"]) != 0 and len(item_data["history"]) > 336:
        item_data["history"].pop(0)

    current_data = {}
    current_data["time"] = bazaar["lastUpdated"]
    try:
        current_data["sellPrice"] = bazaar["products"][item]["buy_summary"][0]["pricePerUnit"]
    except:
        current_data["sellPrice"] = 0
    try:
        current_data["buyPrice"] = bazaar["products"][item]["sell_summary"][0]["pricePerUnit"]
    except:
        current_data["buyPrice"] = 0
    item_data["history"].append(current_data)

    total_sellPrice = 0
    total_buyPrice = 0
    totalCount = len(item_data["history"])
    for data in item_data["history"]:
        total_buyPrice += data["buyPrice"]
        total_sellPrice += data["sellPrice"]
    
    quick_stat[item]["buyPrice"] = total_buyPrice / totalCount
    quick_stat[item]["sellPrice"] = total_sellPrice / totalCount
    
    with open(path, 'w') as f:
        json.dump(item_data, f)

with open(os.path.join(script_path, 'quickstat.json'), 'w') as f:
        json.dump(quick_stat, f)