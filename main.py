from zara import ZaraAvailabilityChecker
from hm import HmAvailabilityChecker
from utils import load_env_variables,ntfy
import json

if __name__ == "__main__":
    load_env_variables()
    jsonfile = open("checklist.json", "r")
    data = json.load(jsonfile)
    for t in data["hm"]:
        _ = HmAvailabilityChecker(t["code"], t["size"]).return_availability()
        if _:
            ntfy(f"New item available: {t['link']}")
    for t in data["zara"]:
        _ = ZaraAvailabilityChecker(t["code"], t["size"]).return_availability()
        if _:
            ntfy(f"New item available: {t['link']}")
    jsonfile.close()