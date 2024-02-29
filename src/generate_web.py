import shutil
import os
import json
from pathlib import Path
from glob import glob, iglob

def inplace_change(input_file, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(input_file) as f:
        s = f.read()
        if old_string not in s:
            print(f"{old_string} not found in {input_file}")
            return

    # Safely write the changed content, if found in the file
    with open(input_file, 'w') as f:
        s = s.replace(old_string, new_string)
        f.write(s)

def main():
    # copy the feeds from feeds/ directory to dist/ directory
    
    # The path to the repo root
    root_path = Path(__file__).parent.parent

    # copy the feed files from /feeds to /dist
    feeds_source = f"{root_path}/feeds"
    feeds_dest = f"{root_path}/dist/feeds"
    shutil.copytree(feeds_source, feeds_dest, dirs_exist_ok=True)    

    # get the feed data from the json files
    feeds = []
    file_list = [f for f in iglob(feeds_source + "/**/*", recursive=True) if os.path.isfile(f) and f.endswith(".json")]
    for f in file_list:
        # read the json
        with open(f, "r") as f_in:
            feeds.append(json.load(f_in))

    # write the table data
    table_data = []
    for feed in feeds:
        print(f"[{feed['title']}] Writing HTML...")
        table_row = f'''<tr>
                <td><a href="{feed['link']}">{feed['title']}</a></td>
                <td><a href="feeds/{ str(feed['title']).lower().replace(' ', '_')}/feed.xml">Feed</a></td>
                <td>{feed["updated"]}</td>
            </tr>'''
        table_data.append(table_row)

    # copy everything in web to the dist
    web_source = f"{root_path}/src/web"
    web_dest = f"{root_path}/dist"
    shutil.copytree(web_source, web_dest, dirs_exist_ok=True)

    # update the index.html file with the table data
    input_file = f"{root_path}/dist/index.html"
    feed_string = "\n".join(str(item) for item in table_data)
    inplace_change(input_file, "<!--FEED_DATA-->", feed_string)


if __name__ == "__main__":
    main()