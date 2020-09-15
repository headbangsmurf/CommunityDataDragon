import download


def get_language_json(lang):
    # Returning Latest DDragon unless we can figure out how to merge trans.json files to match
    return download.download_versioned_ddragon_language(lang)
