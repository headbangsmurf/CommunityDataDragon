import download
import settings


def get_profileicon_json(lang):
    cdragon_profileicons = download.download_versioned_cdragon_profileicons_summary()

    profileicon = {}
    profileicon["type"] = "profileicon"
    profileicon["version"] = settings.patch['json']
    profileicon["data"] = {}
    for x in cdragon_profileicons:
        id = x["id"]
        profileicon["data"][id] = {}
        profileicon["data"][id]["id"] = id
        profileicon["data"][id]["image"] = {}
        profileicon["data"][id]["image"]["full"] = str(id) + ".png"

    return profileicon
