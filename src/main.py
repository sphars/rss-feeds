import json, os, requests, subprocess
from pathlib import Path
from pprint import pprint
from datetime import datetime
from zoneinfo import ZoneInfo

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from sites.thefarside import TheFarSide
from generate_feed import GenerateFeed

def setup_chrome():
    # try and get the chrome version from either the installed chrome or env var
    try:
        chrome_version = subprocess.run(["chromium-browser", "--product-version"],stdout=subprocess.PIPE).stdout.decode("utf-8")
    except:
        chrome_version = os.getenv("CHROME_VERSION", "121.0.6167.184")

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
    chrome_options.enable_downloads = False
    service = Service()
    driver = webdriver.Chrome(options=chrome_options, service=service)
    return driver


def main():

    # setup chrome
    driver = setup_chrome()
    todays_date = datetime.now()

    # run scrapers
    comics_feed_data = []
    tfs = TheFarSide(driver, todays_date)
    tfs_comics = tfs.get_comics()
    comics_feed_data.append(tfs.build_feed_data())
    driver.quit()

    # format final data dictionary
    comics = {
        "date": f"{todays_date.replace(microsecond=0).isoformat()}Z",
        "data": comics_feed_data
    }

    # pprint(comics,indent=2)

    # get the repo root basically
    try:
        path = Path(__file__).parent.parent
    except Exception as e:
        print(e)
    
    for comic_feed in comics_feed_data:
            
        if len(comic_feed["entries"]) > 0:
            comic_slug = comic_feed['title'].replace(' ', '_').lower()

            # write to json file     
            json_file_path = f"{path}/feeds/{comic_slug}/feed.json"
            os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
            try:
                with open(json_file_path, "w") as f:
                    json.dump(comic_feed, f, ensure_ascii=False, indent=2)
            except Exception as e:
                    print(e)

            # write the atom feed
            gf = GenerateFeed()
            atom_feed = gf.generate_atom(comic_feed, todays_date)
            atom_file_path = f"{path}/feeds/{comic_slug}/feed.xml"
            os.makedirs(os.path.dirname(atom_file_path), exist_ok=True)
            try:
                with open(atom_file_path, "w") as f:
                    f.write(atom_feed)
            except Exception as e:
                    print(e)

if __name__ == "__main__":
    main()