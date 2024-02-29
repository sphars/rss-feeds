import shutil
import os
import json
from pathlib import Path
from glob import glob, iglob

def write_template(template_file, destination, old_string, new_string):
    with open(template_file, "rt") as fin:
        s = fin.read()
        if old_string not in s:
            print(f"{old_string} not found in {template_file}")
            return
        with open(destination, "wt") as fout:
            s = s.replace(old_string, new_string)
            fout.write(s)

def main():
    # copy the feeds from feeds/ directory to dist/ directory
    
    # The path to the repo root
    path = Path(__file__).parent.parent

    source = f"{path}/feeds"
    dest = f"{path}/dist/feeds"

    # copy the feed files from /feeds to /dist
    shutil.copytree(source, dest, dirs_exist_ok=True)    

    feeds = []
    file_list = [f for f in iglob(source + "/**/*", recursive=True) if os.path.isfile(f) and f.endswith(".json")]
    print(file_list)
    for f in file_list:
        # read the json
        with open(f, "r") as f_in:
            feeds.append(json.load(f_in))

    # write the table data
    table_data = []
    for feed in feeds:
        table_row = f'''<tr>
            <td><a href="{feed['link']}">{feed['title']}</a></td>
            <td><a href="feeds/{ str(feed['title']).lower().replace(' ', '_')}/feed.xml">Feed</a></td>
            <td>{feed["updated"]}</td>
        </tr>'''
        table_data.append(table_row)

    # update the index.html file
    index_template = f"{path}/src/index_template.html"
    index_file = f"{path}/dist/index.html"
    feed_string = "\n".join(str(item) for item in table_data)
    write_template(index_template, index_file, "<!--FEED_DATA-->", feed_string)


if __name__ == "__main__":
    main()