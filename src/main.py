import json, os, requests
from pprint import pprint
from datetime import datetime
from zoneinfo import ZoneInfo

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from sites.thefarside import TheFarSide

def setup_chrome():
    chrome_version = os.getenv("CHROME_VERSION", "119.0.6045.123")
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

# def get_far_side_comics():
#     todays_date = datetime.now(ZoneInfo("US/Mountain"))


#     far_side_url = f"https://www.thefarside.com/{todays_date.year}/{todays_date.month}/{todays_date.day}"
#     driver.get(far_side_url)
#     driver.implicitly_wait(1)

#     comic_cards = driver.find_elements(By.XPATH, "//div[@data-position]")
#     if comic_cards:
#         print(f"Found {len(comic_cards)} comic cards")
#         comics = []
#         for index, comic_card in enumerate(comic_cards):
#             comic_img = comic_card.find_element(By.TAG_NAME, "img").get_attribute("data-src")
            
#             filepath = f"./comics/thefarside/{todays_date.year}-{todays_date.month}-{todays_date.day}-{index}.jpg"
#             os.makedirs(os.path.dirname(filepath), exist_ok=True)
#             with open(filepath, "wb") as f:
#                 f.write(requests.get(comic_img).content)

#             comic_caption = comic_card.find_element(By.CSS_SELECTOR, ".figure-caption").text
#             comic_data = {
#                 "image": comic_img,
#                 "caption": comic_caption
#             }
#             comics.append(comic_data)

#         return {
#             "date": str(todays_date.isoformat),
#             "comics": comics
#         }
    

def main():
    # run scrapers
    # far_side_comics = get_far_side_comics()
    # pprint(far_side_comics, indent=2)

    driver = setup_chrome()
    todays_date = datetime.now()

    tfs = TheFarSide(driver, todays_date)
    tfs_comics = tfs.get_comics()


    comics = {
        "date": f"{todays_date.replace(microsecond=0).isoformat()}Z",
        "thefarside": tfs_comics
    }

    with open("comics.json", "w") as f:
        json.dump(comics, f, ensure_ascii=False, indent=2)

    pprint(comics,indent=2)

    if (tfs_comics):
        with open("../feeds/thefarside.json", "w") as f:
            json.dump(tfs.build_feed_data(tfs_comics), f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()