import utils
import os
import download
from PIL import Image
import version
import shutil
import constants
import settings


def create_all_images(championfull, items, summoners):
    # Unversioned Images (/cdn/img)
    if(settings.patch['cdragon'] == version.get_latest_cdragon_version() and settings.production == True):
        create_unversioned_champion_splash(championfull)
        create_unversioned_champion_loading(championfull)
        create_unversioned_champion_tile(championfull)
        create_unversioned_perk_images()
        create_unversioned_perk_styles()

    # Versioned Images (/cdn/settings.patch/img)
    create_versioned_champion_icons()
    create_versioned_item_icons(items)
    create_versioned_map_icons()
    create_versioned_mission_assets()
    create_versioned_champion_passives()
    create_versioned_profile_icons()
    create_versioned_spell_icons(championfull, summoners)
    os.system(
        f"./dragonspriter cdn/{settings.patch['json']}/")

    if os.path.exists(f"cdn/{settings.patch['json']}/img/sprite"):
        shutil.rmtree(
            f"cdn/{settings.patch['json']}/img/sprite")
    os.makedirs(
        f"cdn/{settings.patch['json']}/img/sprite")
    os.system(
        f"mv img/sprite/* cdn/{settings.patch['json']}/img/sprite/")
    shutil.rmtree(f"img")


def create_unversioned_champion_splash(championfull):
    if not os.path.exists(f"cdn/img/champion/splash"):
        os.makedirs(f"cdn/img/champion/splash")
    for champion in championfull['data']:
        print(champion)
        champion_key = championfull['data'][champion]['key']

        for i, skin in enumerate(championfull['data'][champion]['skins']):
            print(i)
            image = download.download_versioned_cdragon_champion_splash(
                champion_key, skin['id'])
            print(
                f"{champion}_{championfull['data'][champion]['skins'][i]['num']}"
            )
            with open(f"cdn/img/champion/splash/{champion}_{championfull['data'][champion]['skins'][i]['num']}.jpg", "wb") as f:
                f.write(image)
    return


def create_unversioned_champion_loading(championfull):
    if not os.path.exists(f"cdn/img/champion/loading"):
        os.makedirs(f"cdn/img/champion/loading")
    for champion in championfull['data']:
        champion_key = championfull['data'][champion]['key']
        cdragon_champion = download.download_versioned_cdragon_champion("default",
                                                                        champion_key)
        i = 0
        for x in cdragon_champion['skins']:
            url = get_cdragon_url(x['loadScreenPath'])

            image = utils.download_image(url)
            print(
                f"{champion}_{championfull['data'][champion]['skins'][i]['num']}"
            )
            with open(f"cdn/img/champion/loading/{champion}_{championfull['data'][champion]['skins'][i]['num']}.jpg", "wb") as f:
                f.write(image)
            i += 1
    return


def create_unversioned_champion_tile(championfull):
    if not os.path.exists(f"cdn/img/champion/tiles"):
        os.makedirs(f"cdn/img/champion/tiles")
    for champion in championfull['data']:
        champion_key = championfull['data'][champion]['key']
        cdragon_champion = download.download_versioned_cdragon_champion(
            champion_key)
        i = 0
        for x in cdragon_champion['skins']:
            url = get_cdragon_url(x['tilePath'])

            image = download.download_image(url)
            print(
                f"{champion}_{championfull['data'][champion]['skins'][i]['num']}"
            )
            with open(f"cdn/img/champion/tiles/{champion}_{championfull['data'][champion]['skins'][i]['num']}.jpg", "wb") as f:
                f.write(image)
            i += 1
    return


def create_unversioned_perk_images():
    if not os.path.exists(f"cdn/img/perk-images/Styles"):
        os.makedirs(f"cdn/img/perk-images/Styles")
    cdragon_styles = download.download_versioned_cdragon_perkstyles("default")
    for x in cdragon_styles['styles']:
        url = get_cdragon_url(x['iconPath'])
        image = utils.download_image(url)
        name = get_image_name_from_path(x['iconPath'])
        path = get_path_from_string(x['iconPath'])
        with open(f"cdn/img{path}/{name}", "wb") as f:
            f.write(image)
    return


def create_unversioned_perk_styles():
    cdragon_perks = download.download_versioned_cdragon_perks("default")
    for x in cdragon_perks:
        url = get_cdragon_url(x['iconPath'])
        image = utils.download_image(url)
        path = get_path_from_string(x['iconPath'])
        if not os.path.exists("cdn/img" + path):
            os.makedirs("cdn/img" + path)
        name = get_image_name_from_path(x['iconPath'])
        with open(f"cdn/img{path}/{name}", "wb") as f:
            f.write(image)
    return


def create_versioned_champion_icons():
    if not os.path.exists(f"cdn/{settings.patch['json']}/img/champion"):
        os.makedirs(f"cdn/{settings.patch['json']}/img/champion")
    cdragon_champions = download.download_versioned_cdragon_champion_summary()
    for x in cdragon_champions:
        image = download.download_versioned_cdragon_champion_icon(x['id'])
        with open(f"cdn/{settings.patch['json']}/img/champion/{x['alias']}.png", "wb") as f:
            f.write(image)
    return


def create_versioned_item_icons(items):
    if not os.path.exists(f"cdn/{settings.patch['json']}/img/item"):
        os.makedirs(f"cdn/{settings.patch['json']}/img/item")
    cdragon_items = download.download_versioned_cdragon_items("default")
    for x in cdragon_items:
        if str(x['id']) in items['data']:
            image = download.download_image(
                get_cdragon_url(x['iconPath']))
            with open(f"cdn/{settings.patch['json']}/img/item/{x['id']}.png", "wb") as f:
                f.write(image)
        else:
            print("Skipped " + str(x['id']))
    return


def create_versioned_map_icons():
    if not os.path.exists(f"cdn/{settings.patch['json']}/img/map"):
        os.makedirs(f"cdn/{settings.patch['json']}/img/map")
    cdragon_maps = download.download_versioned_cdragon_map_summary("default")
    for x in cdragon_maps:
        image = download.download_versioned_cdragon_map_icon(x['id'])
        with open(f"cdn/{settings.patch['json']}/img/map/map{x['id']}.png", "wb") as f:
            f.write(image)
    return


def create_versioned_mission_assets():
    if not os.path.exists(f"cdn/{settings.patch['json']}/img/mission"):
        os.makedirs(f"cdn/{settings.patch['json']}/img/mission")
    cdragon_maps = download.download_versioned_cdragon_mission_assets(
        "default")
    for x in cdragon_maps:
        image = download.download_versioned_cdragon_mission_icon(
            get_cdragon_url(x['path']))
        if not os.path.exists(f"cdn/{settings.patch['json']}/img/mission{get_path_from_string(x['path'])}"):
            os.makedirs(
                f"cdn/{settings.patch['json']}/img/mission{get_path_from_string(x['path'])}")
        with open(f"cdn/{settings.patch['json']}/img/mission{get_path_from_string(x['path'])}/{x['internalName']}.png", "wb") as f:
            f.write(image)
    return


def create_versioned_champion_passives():
    if not os.path.exists(f"cdn/{settings.patch['json']}/img/passive"):
        os.makedirs(f"cdn/{settings.patch['json']}/img/passive")
    cdragon_champions = download.download_versioned_cdragon_champion_summary()
    for champion in cdragon_champions:
        cdragon_champion = download.download_versioned_cdragon_champion(
            "default", champion['id'])
        url = get_cdragon_url(cdragon_champion['passive']['abilityIconPath'])
        image = download.download_image(url)
        with open(f"cdn/{settings.patch['json']}/img/passive/{get_image_name_from_path(cdragon_champion['passive']['abilityIconPath'])}", "wb") as f:
            f.write(image)
    return


def create_versioned_profile_icons():
    if not os.path.exists(f"cdn/{settings.patch['json']}/img/profileicon"):
        os.makedirs(f"cdn/{settings.patch['json']}/img/profileicon")
    cdragon_profileicons = download.download_versioned_cdragon_profileicons_summary()
    for x in cdragon_profileicons:
        image = download.download_versioned_cdragon_profile_icon(x['id'])
        with open(f"cdn/{settings.patch['json']}/img/profileicon/{x['id']}.jpg", "wb") as f:
            f.write(image)
        # This conversion process is really long for bulk images.. Will need to improve
        im = Image.open(
            f"cdn/{settings.patch['json']}/img/profileicon/{x['id']}.jpg")
        im.save(f"cdn/{settings.patch['json']}/img/profileicon/{x['id']}.png")
        os.remove(
            f"cdn/{settings.patch['json']}/img/profileicon/{x['id']}.jpg")
    return


def create_versioned_spell_icons(championfull, summoners):
    if not os.path.exists(f"cdn/{settings.patch['json']}/img/spell"):
        os.makedirs(f"cdn/{settings.patch['json']}/img/spell")
    # Champion Spells
    champion_summary = download.download_versioned_cdragon_champion_summary()
    for x in champion_summary:
        champion = download.download_versioned_cdragon_champion(
            "default", x['id'])
        for i, spell in enumerate(champion['spells']):
            image = download.download_image(
                get_cdragon_url(spell['abilityIconPath']))
            name = championfull['data'][x['alias']]['spells'][i]['id']
            with open(f"cdn/{settings.patch['json']}/img/spell/{name}.png", "wb") as f:
                f.write(image)
    # Summoner Spells
    # cdragon_summoners = download.download_versioned_cdragon_summoner_spells(
    #     "default")
    # for x in (x for x in cdragon_summoners if x['name'] != ""):
    return


def get_cdragon_url(path):
    path = path.lower()
    path = path.replace("/lol-game-data/assets/",
                        constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/default/")
    return path


def get_image_name_from_path(path):
    path = path.split("/")
    return path[-1]


def get_path_from_string(path):
    # Need to perfect this function
    path = path.replace("/lol-game-data/assets", "")
    path = path.replace("/v1", "")
    path = path.replace("/ASSETS/Missions", "")
    path_list = path.split("/")
    path = path.replace("/"+path_list[-1], "")
    return path
