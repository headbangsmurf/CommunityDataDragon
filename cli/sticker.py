import settings


def get_sticker_json():
    # This hasn't been included since 9.2.1, so we're not going to include it
    stickers = {
        "type": "sticker",
        "version": settings.patch['json'],
        "data": {},
    }
    return stickers
