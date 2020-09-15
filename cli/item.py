import json
import utils
import download
import settings


def get_item_json(cdragon_language, ddragon_language):
    # Using DDragon info for basic, groups, and tree as these don't seem to be in files anywhere
    ddragon_items = download.download_versioned_ddragon_items(ddragon_language)

    cdragon_items_bin = download.download_versioned_cdragon_items_bin()
    cdragon_items = download.download_versioned_cdragon_items(cdragon_language)
    cdragon_maps = download.download_versioned_cdragon_map_summary(
        cdragon_language)
    maps = {}
    for i in cdragon_maps:
        maps[i['id']] = i['mapStringId']
    items = {
        'type': 'item',
        'version': settings.patch['json'],
        'basic': ddragon_items['basic'],
        'data': {},
        'groups': ddragon_items['groups'],
        'tree': ddragon_items['tree'],
    }

    items["data"] = {}
    for x in cdragon_items:
        item_bin = get_item_bin(x['id'], cdragon_items_bin)
        if x['inStore'] == False and ("mItemDataAvailability" not in item_bin or "{2e97ceab}" not in item_bin['mItemDataAvailability']):
            continue
        id = str(x['id'])
        print(id)

        items['data'][id] = {
            'name': x['name'],
            'description': x['description'],
            # Maybe figure a way to add colloq later but haven't found in CDragon
            'colloq': ddragon_items['data'][id]['colloq'] if "colloq" in ddragon_items['data'][id] else ";",
            'plaintext': "",
        }

        # Can't find in CDragon
        items['data'][id]['plaintext'] = ddragon_items['data'][id]['plaintext'] if "plaintext" in ddragon_items['data'][id] else "",
        if(len(x['from']) > 0):
            items['data'][id]['from'] = x['from']
        if(len(x['to']) > 0):
            items['data'][id]['into'] = x['to']
        items['data'][id]['image'] = {
            'full': str(id) + ".png",
        }
        items['data'][id]['gold'] = {
            'base': x['price'],
            'purchasable': x['inStore'],
            'total': x['priceTotal'],
            'sell': round(x['priceTotal'] * (item_bin['sellBackModifier'] if 'sellBackModifier' in item_bin else 0.7)),
        }
        items['data'][id]['tags'] = x['categories']
        items['data'][id]['maps'] = {}
        for i in maps:
            if maps[i] in x['mapStringIdInclusions']:
                items['data'][id]['maps'][i] = True
            else:
                items['data'][id]['maps'][i] = False
        items['data'][id]['stats'] = {}
        items_bin = get_item_bin(id, cdragon_items_bin)
        for i in items_bin:
            if "Mod" in i and "Mode" not in i:
                if i[0] == "m":
                    items['data'][id]['stats'][i[1:]] = items_bin[i]
                else:
                    items['data'][id]['stats'][i] = items_bin[i]
        if 'mEffectAmount' in items_bin:
            items['data'][id]['effect'] = {}
            index = 0
            for effect in items_bin['mEffectAmount']:
                effect_string = "Effect" + str(index) + "Amount"
                items['data'][id]['effect'][effect_string] = utils.remove_trailing_zeros(
                    effect)
                index += 1
        if 'from' in items['data'][id]:
            items['data'][id]['depth'] = len(items['data'][id]['from'])
        else:
            items['data'][id]['depth'] = 0

        if 'consumed' in items_bin:
            items['data'][id]['consumed'] = True
            if '<consumable>' in items['data'][id]['description']:
                items['data'][id]['consumeOnFull'] = True

        if x['requiredAlly'] != "":
            items['data'][id]['requiredAlly'] = x['requiredAlly']
        if x['requiredChampion'] != "":
            items['data'][id]['requiredChampion'] = x['requiredChampion']

    return items


def get_item_bin(item, cdragon_items_bin):
    for x in cdragon_items_bin:
        if str(cdragon_items_bin[x]['itemID']) == str(item):
            return cdragon_items_bin[x]
    return {}


def add_sprite_info(lang):
    with open(f"cdn/{settings.patch['json']}/spriter_output.json", 'r') as f:
        data = json.load(f)
    with open(f"cdn/{settings.patch['json']}/{lang}/data/item.json", 'r') as f:
        items = json.load(f)
    for item in items['data']:
        items['data'][item]['image'].update({
            'sprite': data['result']['item'][item]['regular']['texture'] + ".png",
            'group': "item",
            'x': data['result']['item'][item]['regular']['x'],
            'y': data['result']['item'][item]['regular']['y'],
            'w': data['result']['item'][item]['regular']['width'],
            'h': data['result']['item'][item]['regular']['height'],
        })
    return items
