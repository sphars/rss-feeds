import xml.etree.ElementTree as ET
from datetime import datetime

class GenerateFeed:
    def __init__(self):
        pass

    def generate_atom(self, comic_json, timestamp: datetime):
        just_the_date_string = timestamp.strftime("%B %d, %Y")

        # create the root element
        feed = ET.Element('feed', attrib={"xmlns": "http://www.w3.org/2005/Atom", "xml:lang": "en"})

        # add feed-level elements
        title = ET.SubElement(feed, "title")
        title.text = comic_json["title"]

        subtitle = ET.SubElement(feed, "subtitle")
        subtitle.text = f"RSS feed for {comic_json['title']}"

        link = ET.SubElement(feed, "link", attrib={"href":f"{comic_json['link']}", "rel":"alternate"})

        id = ET.SubElement(feed, "id")
        id.text = comic_json['id']

        author = ET.SubElement(feed, "author")
        author_name = ET.SubElement(author, "name")
        author_name.text = comic_json['author']

        updated = ET.SubElement(feed, "updated")
        updated.text = comic_json['updated'] # valid ISO timestamp

        # write each comic as an <li> element
        li_elements = []
        for comic_entry in comic_json['entries']:
            li_inner = f'<img src="{comic_entry["summary"]["img"]}" alt="{comic_entry["summary"]["caption"]}"/>'
            li_inner += f"<p>{comic_entry['summary']['caption']}</p>"
            li_element = f"<li>{li_inner}</li>"
            li_elements.append(li_element)

        # write the <ul>
        items = "\n".join(li_elements)
        ul_element = f"<ul>{items}</ul>"

        # Create the entry element
        entry = ET.SubElement(feed, "entry")

        entry_title = ET.SubElement(entry, "title")
        entry_title.text = f"{comic_json['title']} comics for {just_the_date_string}"

        entry_link = ET.SubElement(entry, "link", attrib={"href": comic_json['entries'][0]['link'], "rel":"alternate"})

        entry_id = ET.SubElement(entry, "id")
        entry_id.text = comic_json['entries'][0]['link']

        entry_updated = ET.SubElement(entry, "updated")
        entry_updated.text = comic_json['entries'][0]['updated']  # Use a valid timestamp

        # add the content (<ul>)
        entry_summary = ET.SubElement(entry, "summary", attrib={"type":"html"})
        entry_summary.text = ul_element

        ET.indent(feed, space="\t", level=0)

        # write the string and add a string at the beginning specifying the xml version
        xml_string = ET.tostring(feed, encoding="utf-8", method="xml")
        xml_string = b'<?xml version="1.0" encoding="utf-8"?>\n' + xml_string

        # return the decoded string
        return xml_string.decode('utf-8')