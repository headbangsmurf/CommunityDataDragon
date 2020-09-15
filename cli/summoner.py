import download
import settings


def get_summoner_json(cdragon_language, ddragon_language):
    """
    Creates DDragon summoner.json
    Highly relies on DDragon, could be improved if found on CDragon
    """
    cdragon_summoners = download.download_versioned_cdragon_summoner_spells(
        cdragon_language)
    ddragon_summoners = download.download_versioned_ddragon_summoner_spells(
        ddragon_language)
    summoners = {
        "type": "summoner",
        "version": settings.patch['json'],
        "data": {},
    }
    for x in (x for x in cdragon_summoners if x['name'] != ""):
        try:
            ddragon_spell = get_ddragon_id(x['id'], ddragon_summoners)
            summoners['data'].update({
                ddragon_spell['id']: {
                    "id": ddragon_spell['id'],
                    "name": x['name'],
                    "description": x['description'],
                    "tooltip": ddragon_spell['tooltip'],
                    "maxrank": 1,
                    "cooldown": [x['cooldown']],
                    "cooldownBurn": str(x['cooldown']),
                    "datavalues": {},
                    "effect": ddragon_spell['effect'],
                    "effectBurn": ddragon_spell['effectBurn'],
                    "vars": ddragon_spell['vars'],
                    "key": str(x['id']),
                    "summonerLevel": x['summonerLevel'],
                    "modes": x['gameModes'],
                    "costType": ddragon_spell['costType'],
                    "maxammo": ddragon_spell['maxammo'],
                    "range": ddragon_spell['range'],
                    "rangeBurn": ddragon_spell['rangeBurn'],
                    "image": {
                        "full": ddragon_spell['id'] + ".png"
                    },
                    "resource": ddragon_spell['resource'],
                }
            })
        except:
            print("Failure on Summoner Spell: " + x['name'])
            continue

    return summoners


def get_ddragon_id(cdragon_id, ddragon_summoners):
    """
    Gets summoner spell from DDragon from CDragon numeric ID
    """
    for x in ddragon_summoners['data']:
        if ddragon_summoners['data'][x]['key'] == str(cdragon_id):
            return ddragon_summoners['data'][x]
    return {}
