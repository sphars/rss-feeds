import json, os, requests, subprocess
from pprint import pprint
from datetime import datetime
from zoneinfo import ZoneInfo

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from sites.thefarside import TheFarSide

def setup_chrome():
    # try and get the chrome version from either the installed chrome or env var
    try:
        chrome_version = subprocess.run(["google-chrome", "--product-version"],stdout=subprocess.PIPE).stdout.decode("utf-8")
    except:
        chrome_version = os.getenv("CHROME_VERSION", "120.0.6099.129")

    print(f"Using Chrome {chrome_version}")
    chrome_options = webdriver.ChromeOptions()
    user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36"
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1080",
        "--disable-extensions",
        "--no-sandbox",
        f"--user-agent={user_agent}"
    ]
    for option in options:
        chrome_options.add_argument(option)
    chrome_options.enable_downloads = True
    service = Service(log_output=1)
    driver = webdriver.Chrome(options=chrome_options, service=service)
    return driver


def main():

    # setup chrome
    driver = setup_chrome()
    todays_date = datetime.now()

    # run scrapers
    tfs = TheFarSide(driver, todays_date)
    tfs_comics = tfs.get_comics()


    # format
    comics = {
        "date": f"{todays_date.replace(microsecond=0).isoformat()}Z",
        "thefarside": tfs_comics
    }

    with open("comics.json", "w") as f:
        json.dump(comics, f, ensure_ascii=False, indent=2)

    pprint(comics,indent=2)

    # write to json file
    if (tfs_comics):
        with open("../feeds/thefarside.json", "w") as f:
            json.dump(tfs.build_feed_data(tfs_comics), f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()