import os
import utils
from natsort import natsorted

def update_api():
    if not os.path.exists("api"):
        os.makedirs("api")
        
    create_version()
    

def create_version():
    patches = [f.path.split("/")[1] for f in os.scandir("cdn") if f.is_dir() and "img" not in f.path]
    patches = natsorted(patches)
    patches.reverse()
    utils.save_json(patches, "api/versions.json")

update_api()