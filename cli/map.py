import download
import json
import settings


def get_map_json(lang):
    cdragon_maps = download.download_versioned_cdragon_map_summary(lang)
    maps = {
        "type": "map",
        "version": settings.patch['json'],
        "data": {},
    }
    for x in cdragon_maps:
        id = x["id"]
        maps["data"][id] = {
            "MapName": x['name'],
            "MapId": str(id),
            "image": {
                'full': "map" + str(id) + ".png",
            },
        }
    return maps


def add_sprite_info(lang):
    with open(f"cdn/{settings.patch['json']}/spriter_output.json", 'r') as f:
        data = json.load(f)
    with open(f"cdn/{settings.patch['json']}/{lang}/data/map.json", 'r') as f:
        maps = json.load(f)
    for map in maps['data']:
        maps['data'][map]['image'].update({
            'sprite': data['result']['map'][map]['regular']['texture'] + ".png",
            'group': "map",
            'x': data['result']['map'][map]['regular']['x'],
            'y': data['result']['map'][map]['regular']['y'],
            'w': data['result']['map'][map]['regular']['width'],
            'h': data['result']['map'][map]['regular']['height'],
        })
    return maps
