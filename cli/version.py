import utils
import constants


def get_latest_ddragon_version():
    versions = utils.download_json(
        constants.ddragon_url + "/api/versions.json")
    versions = [v for v in versions if "_" not in v]
    return versions[0]


def get_ddragon_version(patch):
    versions = utils.download_json(
        constants.ddragon_url + "/api/versions.json")
    versions = [v for v in versions if "_" not in v]
    for v in versions:
        if v.startswith(patch):
            return v
    return versions[0]


def get_latest_cdragon_version():
    versionstring = utils.download_json(
        constants.cdragon_url + "/latest/content-metadata.json")['version']
    split = versionstring.split(".")
    return f"{split[0]}.{split[1]}"


def get_cdragon_version(patch):
    versions = utils.download_json(constants.cdragon_url + "/json/")
    for v in versions:
        if patch == v['name']:
            return v['name']
    raise Exception('Invalid patch specified')
