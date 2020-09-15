import argparse
import version
import sys

args = []
patch = {}


def init():
    global patch
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-patch", "-p", help="generate ddragon from specific patch", default="latest")
    args = parser.parse_args()

    if args.patch == "latest":
        patch = {
            'ddragon': version.get_latest_ddragon_version(),
            'cdragon': version.get_latest_cdragon_version(),
            'json': version.get_latest_cdragon_version() + ".1",
        }
    elif args.patch == "pbe":
        patch = {
            'ddragon': version.get_latest_ddragon_version(),
            'cdragon': version.get_cdragon_version(args.patch),
            'json': "pbe",
        }
    else:
        patch = {
            'ddragon': version.get_ddragon_version(args.patch),
            'cdragon': version.get_cdragon_version(args.patch),
            'json': version.get_cdragon_version(args.patch) + ".1",
        }
