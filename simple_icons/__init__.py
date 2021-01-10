# type: ignore[attr-defined]
"""A small python wrapper for the https://github.com/simple-icons/simple-icons/ project"""

from pathlib import Path
import json
import re
import xmltodict


class IconNotFoundException(Exception):
    """Icon not found Exception."""


def title_to_filename(title):
    title = re.sub(r"/\+/g", "plus", title.lower())
    title = re.sub(r"/^\./", "dot-", title)
    title = re.sub(r"/\.$/", "-dot", title)
    title = re.sub(r"/\./g", "-dot-", title)
    title = re.sub(r"/^&/", "and-", title)
    title = re.sub(r"/&$/", "-and", title)
    title = re.sub(r"/&/g", "-and-", title)
    title = re.sub(r"/[ !:’'°]/g", "", title)
    title = re.sub(r"/à|á|â|ã|ä/g", "a", title)
    title = re.sub(r"/ç|č|ć/g", "c", title)
    title = re.sub(r"/è|é|ê|ë/g", "e", title)
    title = re.sub(r"/ì|í|î|ï/g", "i", title)
    title = re.sub(r"/ñ|ň|ń/g", "n", title)
    title = re.sub(r"/ò|ó|ô|õ|ö/g", "o", title)
    title = re.sub(r"/š|ś/g", "s", title)
    title = re.sub(r"/ù|ú|û|ü/g", "u", title)
    title = re.sub(r"/ý|ÿ/g", "y", title)
    title = re.sub(r"/ž|ź/g", "z", title)

    return title


data = None

with open(
    Path(f"si-source/_data/simple-icons.json").resolve(),
    mode="r",
    encoding="utf-8",
    errors="ignore",
) as file:
    raw = json.loads(file.read())

    data = {
        title_to_filename(dat.get("title")): dat for dat in raw.get("icons")
    }


def get_svg(icon):

    path = Path(f"si-source/icons/{icon}.svg").resolve()

    try:
        with open(path, mode="r", encoding="utf-8", errors="ignore") as file:
            svg = file.read()
    except Exception as exception:
        raise IconNotFoundException()

    return svg


def get_data(icon):
    return data.get(icon)


def get_icon(icon):
    data = get_data(icon)
    svg = get_svg(icon)

    svg_data = xmltodict.parse(svg)

    view_box = svg_data.get("svg").get("@viewBox")
    path = svg_data.get("svg").get("path").get("@d")

    data.update({"view_box": view_box, "path": path})

    return data
