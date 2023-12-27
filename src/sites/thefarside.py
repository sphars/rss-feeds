import os, requests
from datetime import datetime

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class TheFarSide:

    comics = []

    def __init__(self, driver: Chrome, todays_date: datetime):
        self.driver = driver
        self.todays_date = todays_date

    # def write_image(self, filepath, img):
    #     os.makedirs(os.path.dirname(filepath), exist_ok=True)
    #     with open(filepath, "wb") as f:
    #         f.write(requests.get(img).content)

    def get_comics(self):
        # day string should be YYYY/MM/DD
        current_day_string = self.todays_date.strftime("%Y/%m/%d")
        far_side_url = f"https://www.thefarside.com/{current_day_string}"
        
        self.driver.get(far_side_url)
        self.driver.implicitly_wait(2)

        comic_cards = self.driver.find_elements(By.XPATH, "//div[@data-position]")
        if comic_cards:
            print(f"Found {len(comic_cards)} comic cards")
            
            comics = []
            for index, comic_card in enumerate(comic_cards):
                comic_img_url = comic_card.find_element(By.TAG_NAME, "img").get_attribute("data-src")
                
                # filepath = f"./comics/{todays_date.year}-{todays_date.month}-{todays_date.day}-{index}.jpg"
                # self.write_image(filepath, comic_img_url)

                # some comics don't have a caption so handle it
                try:
                    comic_caption = comic_card.find_element(By.CSS_SELECTOR, ".figure-caption").text
                except NoSuchElementException:
                    comic_caption = ""

                comic_data = {
                    "image": comic_img_url,
                    "caption": comic_caption
                }
                comics.append(comic_data)

            self.comics = comics
            return comics
        
    def build_feed_data(self, comics):
        entries = []

        for index, comic in enumerate(comics):
            entry = {
                "title": f"The Far Side comic {index + 1} for {self.todays_date.strftime('%B %d, %Y')}",
                "link": f"https://www.thefarside.com/{self.todays_date.year}/{self.todays_date.month}/{self.todays_date.day}",
                "updated": f"{self.todays_date.replace(microsecond=0).isoformat()}Z",
                "id": f"https://www.thefarside.com/{self.todays_date.year}/{self.todays_date.month}/{self.todays_date.day}",
                "summary": {
                    "img": comic["image"],
                    "caption": comic["caption"]
                }
            }
            entries.append(entry)

        feed_data = {
            "title": "The Far Side",
            "link": "https://www.thefarside.com/",
            "id": "https://www.thefarside.com/",
            "updated": f"{self.todays_date.replace(microsecond=0).isoformat()}Z",
            "author": "Gary Larson",
            "entries": entries
        }

        return feed_data
        