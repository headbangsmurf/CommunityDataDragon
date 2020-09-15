import os
import json
import utils
import champion
import item
import map
import mission
import profileicon
import runesreforged
import language
import sticker
import summoner
import tarfile
import images
import version
import settings

import sys

# Files to solve:
# champion/individual champion Files
# champion.json X
# championFull.json X
# item.json X
# language.json
# map.json X
# mission-assets.json
# profileicon.json
# runesReforged.json
# sticker.json
# summoner.json

path = ""


def main():
    languages = {
        'cs_CZ': 'cs_cz',
        'de_DE': 'de_de',
        'el_GR': 'el_gr',
        'en_AU': 'en_au',
        'en_GB': 'en_gb',
        'en_PH': 'en_ph',
        'en_SG': 'en_sg',
        'en_US': 'default',
        'es_AR': 'es_ar',
        'es_ES': 'es_es',
        'es_MX': 'es_mx',
        'fr_FR': 'fr_fr',
        'hu_HU': 'hu_hu',
        'it_IT': 'it_it',
        'ja_JP': 'ja_jp',
        'ko_KR': 'ko_kr',
        'pl_PL': 'pl_pl',
        'pt_BR': 'pt_br',
        'ro_RO': 'ro_ro',
        'ru_RU': 'ru_ru',
        'th_TH': 'th_th',
        'tr_TR': 'tr_tr',
        'vn_VN': 'vn_vn',
        'zh_CN': 'zh_cn',
        'zh_MY': 'zh_my',
        'zh_TW': 'zh_tw',
    }

    # directory = os.path.abspath(os.path.join(
    #     os.path.dirname(os.path.realpath(__file__)), "../.."))

    # No new updated patch, die
    # if os.path.exists(f"cdn/{settings.patch['json']}"):
    #     sys.exit("No new patch exists")

    if not os.path.exists(f"cdn/{settings.patch['json']}"):
        os.makedirs(f"cdn/{settings.patch['json']}")
    for lang in languages:
        print(lang)
        if not os.path.exists(f"cdn/{settings.patch['json']}/{lang}"):
            os.mkdir(f"cdn/{settings.patch['json']}/{lang}")
        path = f"cdn/{settings.patch['json']}/{lang}/data"
        if not os.path.exists(path):
            os.mkdir(path)

        # champions = champion.get_champion_json(languages[lang])
        # utils.save_json(champions, path+'/champion.json')
        # championfull = champion.get_championfull_json(languages[lang], lang)
        # utils.save_json(championfull, path+'/championFull.json')
        championfull = champion.generate_champion_jsons(languages[lang], lang)
        items = item.get_item_json(languages[lang], lang)
        utils.save_json(items, path+"/item.json")
        maps = map.get_map_json(languages[lang])
        utils.save_json(maps, path+"/map.json")
        missions = mission.get_mission_json(languages[lang])
        utils.save_json(missions, path+"/misson-assets.json")
        profileicons = profileicon.get_profileicon_json(languages[lang])
        utils.save_json(profileicons, path+"/profileicon.json")
        runesreforgedjson = runesreforged.get_runesreforged_json(
            languages[lang])
        utils.save_json(runesreforgedjson, path+"/runesReforged.json")
        summoners = summoner.get_summoner_json(languages[lang], lang)
        utils.save_json(summoners, path+"/summoner.json")
        languages_json = language.get_language_json(lang)
        utils.save_json(languages_json, path+"/language.json")
        stickers = sticker.get_sticker_json()
        utils.save_json(stickers, path+"/sticker.json")

    images.create_all_images(championfull, items, summoners)
    for lang in languages:
        path = f"cdn/{settings.patch['json']}/{lang}/data"
        championfull = champion.add_sprite_info(lang)
        utils.save_json(championfull, path+'/championFull.json')
        items = item.add_sprite_info(lang)
        utils.save_json(items, path+'/item.json')

    # with tarfile.open('cdn/dragontail-' + settings.patch + '.tgz', mode='w:gz') as archive:
    #     archive.add('cdn/'+settings.patch, arcname=settings.patch)


if __name__ == "__main__":
    settings.init()
    main()
