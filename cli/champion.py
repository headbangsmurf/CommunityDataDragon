import utils
import json
import download
import settings
import utils
import os


def generate_champion_jsons(cdragon_language, ddragon_language):
    get_champion_json(cdragon_language, ddragon_language)
    championfull = get_championfull_json(cdragon_language, ddragon_language)
    get_individual_champion_json(
        cdragon_language, ddragon_language, championfull)
    return championfull


def get_champion_json(cdragon_language, ddragon_language):
    cdragon_champions = download.download_versioned_cdragon_champion_summary()
    champions = {
        'type': 'champion',
        'format': 'standAloneComplex',
        'version': settings.patch['json'],
    }
    champions["data"] = {}
    for champion in cdragon_champions:
        champions['data'][champion['alias']] = {
            "version": settings.patch['json'],
            'id': champion['alias'],
            'key': str(champion['id']),

        }

    for champion in champions["data"]:
        print(champion)
        cdragon_champion = download.download_versioned_cdragon_champion(
            cdragon_language, champions['data'][champion]['key'])
        cdragon_bin = download.download_versioned_cdragon_champion_bin(
            champion)
        champions['data'][champion].update({
            'name': if_key_exists('name', cdragon_champion),
            'title': if_key_exists('title', cdragon_champion),
            'blurb': blurb(cdragon_champion['shortBio']),
            'info': {
                'attack': if_key_exists('attackRank', cdragon_bin['characterToolData']),
                'defense': if_key_exists('defenseRank', cdragon_bin['characterToolData']),
                'magic': if_key_exists('magicRank', cdragon_bin['characterToolData']),
                'difficulty': if_key_exists('difficultyRank', cdragon_bin['characterToolData']),
            },
            'image': {
                'full': cdragon_champion['alias'] + '.png'
                # Need Sprite Sheets
            },
            'tags': list(map(lambda x: x.title(), cdragon_champion['roles'])),
            'partype': get_partype(cdragon_bin).title(),
            'stats': {
                'hp': cdragon_bin['baseHP'],
                'hpperlevel': cdragon_bin['hpPerLevel'],
                'mp': round(if_key_exists('arBase', cdragon_bin['primaryAbilityResource']), 3),
                'mpperlevel': if_key_exists('arPerLevel', cdragon_bin['primaryAbilityResource']),
                'movespeed': cdragon_bin['baseMoveSpeed'],
                'armor': round(cdragon_bin['baseArmor'], 3),
                'armorperlevel': if_key_exists('armorPerLevel', cdragon_bin),
                'spellblock': round(cdragon_bin['baseSpellBlock'], 3),
                'spellblockperlevel': cdragon_bin['spellBlockPerLevel'],
                'attackrange': cdragon_bin['attackRange'],
                'hpregen': round(if_key_exists('baseStaticHPRegen', cdragon_bin) * 5, 3),
                'hpregenperlevel': round(cdragon_bin['hpRegenPerLevel'] * 5, 3),
                'mpregen': round(if_key_exists('arBaseStaticRegen', cdragon_bin['primaryAbilityResource']) * 5, 3),
                'mpregenperlevel': round(if_key_exists('arRegenPerLevel', cdragon_bin['primaryAbilityResource']) * 5, 3),
                'crit': 0,
                'critperlevel': 0,
                'attackdamage': round(cdragon_bin['baseDamage'], 3),
                'attackdamageperlevel': round(if_key_exists('damagePerLevel', cdragon_bin), 3),
                'attackspeedperlevel': round(if_key_exists('attackSpeedPerLevel', cdragon_bin), 3),
                'attackspeed': round(cdragon_bin['attackSpeed'], 3),
            },
        })
    utils.save_json(
        champions, f"cdn/{settings.patch['json']}/{ddragon_language}/data/champion.json")
    return champions


def get_championfull_json(cdragon_language, ddragon_language):
    cdragon_champions = download.download_versioned_cdragon_champion_summary()
    ddragon_champions = download.download_versioned_ddragon_championfull(
        ddragon_language)
    champions = {
        'type': 'champion',
        'format': 'full',
        'version': settings.patch['json'],
        "data": {},
        "keys": {},
    }
    champions["data"] = {}
    for champion in cdragon_champions:
        champions['data'][champion['alias']] = {
            'id': champion['alias'],
            'key': champion['id'],
        }
        champions['keys'][champion['id']] = champion['alias']

    for champion in champions["data"]:
        print(champion)
        id = champions["data"][champion]["key"]
        cdragon_champion = download.download_versioned_cdragon_champion(
            cdragon_language, id)
        cdragon_bin = download.download_versioned_cdragon_champion_bin(
            champion)
        champions['data'][champion].update({
            'name': cdragon_champion['name'],
            'title': cdragon_champion['title'],
            'image': {
                'full': cdragon_champion['alias'] + '.png'
            },
            'skins': {
            },
            'lore': cdragon_champion['shortBio'],
            'blurb': blurb(cdragon_champion['shortBio']),
            # Missing tips, where to pull these from? Character_Aatrox_Tips
            "allytips": [],
            "enemytips": [],
            'tags': list(map(lambda x: x.title(), cdragon_champion['roles'])),
            'partype': get_partype(cdragon_bin).title(),
            'info': {
                'attack': if_key_exists('attackRank', cdragon_bin['characterToolData']),
                'defense': if_key_exists('defenseRank', cdragon_bin['characterToolData']),
                'magic': if_key_exists('magicRank', cdragon_bin['characterToolData']),
                'difficulty': if_key_exists('difficultyRank', cdragon_bin['characterToolData']),
            },
            'stats': {
                'hp': cdragon_bin['baseHP'],
                'hpperlevel': cdragon_bin['hpPerLevel'],
                'mp': round(if_key_exists('arBase', cdragon_bin['primaryAbilityResource']), 3),
                'mpperlevel': if_key_exists('arPerLevel', cdragon_bin['primaryAbilityResource']),
                'movespeed': cdragon_bin['baseMoveSpeed'],
                'armor': round(cdragon_bin['baseArmor'], 3),
                'armorperlevel': if_key_exists('armorPerLevel', cdragon_bin),
                'spellblock': round(cdragon_bin['baseSpellBlock'], 3),
                'spellblockperlevel': cdragon_bin['spellBlockPerLevel'],
                'attackrange': cdragon_bin['attackRange'],
                'hpregen': round(if_key_exists('baseStaticHPRegen', cdragon_bin) * 5, 3),
                'hpregenperlevel': round(cdragon_bin['hpRegenPerLevel'] * 5, 3),
                'mpregen': round(if_key_exists('arBaseStaticRegen', cdragon_bin['primaryAbilityResource']) * 5, 3),
                'mpregenperlevel': round(if_key_exists('arRegenPerLevel', cdragon_bin['primaryAbilityResource']) * 5, 3),
                'crit': 0,
                'critperlevel': 0,
                'attackdamage': round(cdragon_bin['baseDamage'], 3),
                'attackdamageperlevel': round(if_key_exists('damagePerLevel', cdragon_bin), 3),
                'attackspeedperlevel': round(if_key_exists('attackSpeedPerLevel', cdragon_bin), 3),
                'attackspeed': round(cdragon_bin['attackSpeed'], 3),
            },
            'spells': [],
            'passive': {
                'name': cdragon_champion['passive']['name'],
                'description': cdragon_champion['passive']['description'],
                'image': {
                    'full': get_icon_name(cdragon_champion['passive']['abilityIconPath'])
                },
            },
            'recommended': [],  # Pull these from CDragon Files
        })
        champions['data'][champion]['skins'] = []
        for y, i in enumerate(cdragon_champion["skins"]):
            skin_num = get_skin_num(id, cdragon_champion["skins"][y]['id'])
            skin = {
                'id': cdragon_champion["skins"][y]['id'],
                'num': skin_num,
                'name': cdragon_champion["skins"][y]['name'] if cdragon_champion["skins"][y]['isBase'] != True else "default",
                'chromas': True if 'chromaPath' in cdragon_champion["skins"][y] else False,
            }
            champions['data'][champion]['skins'].append(skin)

        y = 0
        for x in cdragon_champion['spells']:
            spell = {}
            spell['id'] = cdragon_bin['spellNames'][y].split(
                "/")[-1]
            cdragon_ability_bin = download.download_versioned_cdragon_champion_bin_ability(
                champion, spell['id'])
            spell['name'] = cdragon_champion['spells'][y]['name']
            spell['description'] = cdragon_champion['spells'][y]['description']
            # The modifiers in CDragon don't match DDragon
            spell['tooltip'] = cdragon_champion['spells'][y]['dynamicDescription']
            spell['leveltip'] = {}  # Add this
            try:
                spell['maxrank'] = cdragon_ability_bin['mSpell']['mClientData']['mTooltipData']['mLists']['LevelUp']['levelCount']
            except:
                spell['maxrank'] = 6  # Aphelios
            spell['cooldown'] = {}
            spell['cooldownBurn'] = ""
            # Ults there are 5 when you only have 3 levels and the maxLevel is always 0 on CDrag
            for i in range(spell['maxrank']):
                spell['cooldown'][i] = cdragon_champion['spells'][y]['cooldownCoefficients'][i]
                spell['cooldownBurn'] = spell['cooldownBurn'] + remove_trailing_zeros(
                    cdragon_champion['spells'][y]['cooldownCoefficients'][i]) + "/"  # Burns need to be fixed so that if they are the same they are merged
            spell['cooldownBurn'] = get_burn_string(spell['cooldownBurn'])
            spell['cost'] = {}
            spell['costBurn'] = ""
            for i in range(spell['maxrank']):
                spell['cost'][i] = cdragon_champion['spells'][y]['costCoefficients'][i]
                spell['costBurn'] = spell['costBurn'] + \
                    remove_trailing_zeros(
                        cdragon_champion['spells'][y]['costCoefficients'][i]) + "/"
            spell['costBurn'] = get_burn_string(spell['costBurn'])
            spell['datavalues'] = {}
            spell['effect'] = {}
            spell['effectBurn'] = {}

            for i in range(11):
                if i == 0:
                    spell['effect'][i] = None
                    spell['effectBurn'][i] = None
                    continue
                spell['effectBurn'][i] = ""
                spell['effect'][i] = {}
                for j in range(5):
                    spell['effect'][i][j] = cdragon_champion[
                        'spells'][y]['effectAmounts'][f'Effect{i}Amount'][j]
                    spell['effectBurn'][i] = spell['effectBurn'][i] + \
                        remove_trailing_zeros(
                            cdragon_champion['spells'][y]['effectAmounts'][f'Effect{i}Amount'][j]) + "/"
                spell['effectBurn'][i] = get_burn_string(
                    spell['effectBurn'][i])
            spell['vars'] = {}
            j = 0
            for i in cdragon_champion['spells'][y]['coefficients']:
                if cdragon_champion['spells'][y]['coefficients'][i] != 0:
                    spell['vars'][j] = {}
                    spell['vars'][j]['link'] = "spelldamage"
                    spell['vars'][j]['coeff'] = cdragon_champion['spells'][y]['coefficients'][i]
                    # Will need to figure out keys later
                    spell['vars'][j]['key'] = "a1"
                    j += 1
            # This seems like it is always this string
            spell['costType'] = " {{ abilityresourcename }}"
            # This seems like it is always this string
            spell['maxammo'] = "-1"
            spell['range'] = {}
            spell['rangeBurn'] = ""
            for i in range(len(cdragon_champion['spells'][y]['range']) - 1):
                spell['range'][i] = cdragon_champion['spells'][y]['range'][i]
                spell['rangeBurn'] = spell['rangeBurn'] + remove_trailing_zeros(
                    cdragon_champion['spells'][y]['range'][i]) + "/"  # Burns need to be fixed so that if they are the same they are merged
            spell['rangeBurn'] = get_burn_string(spell['rangeBurn'])
            spell['image'] = {}
            # Need Sprite Sheets Here if possible
            spell['image']['full'] = spell['id'] + ".png"
            champions['data'][champion]['spells'].append(spell)
            y += 1
        for x in cdragon_champion['recommendedItemDefaults']:
            champions['data'][champion]['recommended'].append(
                download.download_versioned_cdragon_recommended(x))
        try:
            champions['data'][champion]['allytips'] = ddragon_champions['data'][champion]['allytips']
            champions['data'][champion]['enemytips'] = ddragon_champions['data'][champion]['enemytips']
        except:
            print("ddragon failed")

    utils.save_json(
        champions, f"cdn/{settings.patch['json']}/{ddragon_language}/data/championFull.json")
    return champions


def get_individual_champion_json(cdragon_language, ddragon_language, championfull):
    if not os.path.exists(f"cdn/{settings.patch['json']}/{ddragon_language}/data/champion"):
        os.makedirs(
            f"cdn/{settings.patch['json']}/{ddragon_language}/data/champion")
    for x in championfull['data']:
        champion = {
            "type": "champion",
            "format": "standAloneComplex",
            "version": settings.patch['json'],
            "data": {
                x: championfull['data'][x],
            },
        }
        utils.save_json(
            champion, f"cdn/{settings.patch['json']}/{ddragon_language}/data/champion/{x}.json")


def add_sprite_info(lang):
    """
    Adds Sprite Info to JSONs
    """
    data = utils.load_json(f"cdn/{settings.patch['json']}/spriter_output.json")

    # champion.json
    champions = utils.load_json(
        f"cdn/{settings.patch['json']}/{lang}/data/champion.json")
    for champion in champions['data']:
        champions['data'][champion]['image'].update({
            'sprite': data['result']['champion'][champion]['regular']['texture'] + ".png",
            'group': "champion",
            'x': data['result']['champion'][champion]['regular']['x'],
            'y': data['result']['champion'][champion]['regular']['y'],
            'w': data['result']['champion'][champion]['regular']['width'],
            'h': data['result']['champion'][champion]['regular']['height'],
        })
    utils.save_json(
        champions, f"cdn/{settings.patch['json']}/{lang}/data/champion.json")

    # championFull.json
    championfull = utils.load_json(
        f"cdn/{settings.patch['json']}/{lang}/data/championFull.json")
    for champion in championfull['data']:
        championfull['data'][champion]['image'].update({
            'sprite': data['result']['champion'][champion]['regular']['texture'] + ".png",
            'group': "champion",
            'x': data['result']['champion'][champion]['regular']['x'],
            'y': data['result']['champion'][champion]['regular']['y'],
            'w': data['result']['champion'][champion]['regular']['width'],
            'h': data['result']['champion'][champion]['regular']['height'],
        })
        for spell in championfull['data'][champion]['spells']:
            spell_id = spell['id']
            spell['image'].update({
                'sprite': data['result']['spell'][spell_id]['regular']['texture'] + ".png",
                'group': "spell",
                'x': data['result']['spell'][spell_id]['regular']['x'],
                'y': data['result']['spell'][spell_id]['regular']['y'],
                'w': data['result']['spell'][spell_id]['regular']['width'],
                'h': data['result']['spell'][spell_id]['regular']['height'],
            })
        passive = championfull['data'][champion]['passive']['image']['full'].split(".png")[
            0]
        championfull['data'][champion]['passive']['image'].update({
            'sprite': data['result']['passive'][passive]['regular']['texture'] + ".png",
            'group': "passive",
            'x': data['result']['passive'][passive]['regular']['x'],
            'y': data['result']['passive'][passive]['regular']['y'],
            'w': data['result']['passive'][passive]['regular']['width'],
            'h': data['result']['passive'][passive]['regular']['height'],
        })
    utils.save_json(
        championfull, f"cdn/{settings.patch['json']}/{lang}/data/championFull.json")

    # Individual Champion JSONs
    for champion in champions['data']:
        champion_json = utils.load_json(
            f"cdn/{settings.patch['json']}/{lang}/data/champion/{champion}.json")
        champion_json['data'][champion]['image'].update({
            'sprite': data['result']['champion'][champion]['regular']['texture'] + ".png",
            'group': "champion",
            'x': data['result']['champion'][champion]['regular']['x'],
            'y': data['result']['champion'][champion]['regular']['y'],
            'w': data['result']['champion'][champion]['regular']['width'],
            'h': data['result']['champion'][champion]['regular']['height'],
        })
        utils.save_json(
            champion_json, f"cdn/{settings.patch['json']}/{lang}/data/champion/{champion}.json")
    return championfull


def get_alias(champion):
    return champion.get('alias')


def if_key_exists(key, dictionary):
    if key in dictionary:
        return dictionary[key]
    return 0


def get_partype(cdragon_bin):
    # Need to find a better way to do this as this doesn't transfer between languages
    if 'arType' not in cdragon_bin['primaryAbilityResource']:
        return 'None'
    elif cdragon_bin['primaryAbilityResource']['arType'] == 0:
        return 'Mana'
    elif cdragon_bin['primaryAbilityResource']['arType'] == 1:
        return 'Energy'
    elif cdragon_bin['primaryAbilityResource']['arType'] == 3:
        return 'Shield'
    elif cdragon_bin['primaryAbilityResource']['arType'] == 4 or cdragon_bin['primaryAbilityResource']['arType'] == 5 or cdragon_bin['primaryAbilityResource']['arType'] == 6:
        return 'Fury'
    elif cdragon_bin['primaryAbilityResource']['arType'] == 7:
        return 'Heat'
    elif cdragon_bin['primaryAbilityResource']['arType'] == 8:
        if 'arIncrements' not in cdragon_bin['primaryAbilityResource']:
            return 'Rage'
        elif cdragon_bin['primaryAbilityResource']['arIncrements'] == 0:
            return 'Grit'
        elif cdragon_bin['primaryAbilityResource']['arIncrements'] == 1:
            return 'Crimson Rush'
        elif cdragon_bin['primaryAbilityResource']['arIncrements'] > 1:
            return 'Rage'
    elif cdragon_bin['primaryAbilityResource']['arType'] == 9:
        return 'Ferocity'
    elif cdragon_bin['primaryAbilityResource']['arType'] == 10:
        return 'Blood Well'
    elif cdragon_bin['primaryAbilityResource']['arType'] == 11:
        return 'Flow'
    else:
        return 'Unknown'


def blurb(bio):
    bio = bio[0:255]
    return ' '.join(bio.split(' ')[:-1]) + '...'


def remove_trailing_zeros(x):
    return str(x).rstrip('0').rstrip('.')


def get_icon_name(x):
    return x.split('/')[-1]


def get_skin_num(id, skin_id):
    skin = str(id)
    length = len(skin)
    new_id = str(skin_id)[length:]
    return int(new_id)


def get_burn_string(burn_string):
    new_burn = ""
    burn_list = burn_string.split("/")[:-1]
    res = []
    [res.append(x) for x in burn_list if x not in res]
    for burn in res:
        new_burn = new_burn + burn + "/"
    return new_burn[:-1]
