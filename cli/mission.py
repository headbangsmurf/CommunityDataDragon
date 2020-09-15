import settings
import download


def get_mission_json(lang):
    cdragon_missions = download.download_cdragon_mission_assets(lang)
    missions = {
        "type": "mission",
        "version": settings.patch['json'],
        "data": {},
    }
    for x in cdragon_missions:
        id = x["internalName"]
        missions["data"][id] = {}
        # One of these is 10, not sure where that comes from
        missions["data"][id]['id'] = 0
        missions["data"][id]['image'] = {}
        missions["data"][id]['image']['full'] = str(id) + ".png"

    return missions
