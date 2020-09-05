from jinja2 import (FileSystemLoader,
                    Environment,
                    environment)
from typing import Dict
from pathlib import Path
from urllib.parse import urldefrag


def urlfragment(value):
    subject = urldefrag(url=value).fragment  # after hash
    return subject


def load_template(template: str):
    f_loader = FileSystemLoader(Path(__file__).parent / 'templates')
    env = Environment(loader=f_loader)
    template_obj = env.get_template(template)
    return template_obj


def render_template(template: str, ns: str, item: Dict, item_name: str) -> str:
    environment.DEFAULT_FILTERS['urlfragment'] = urlfragment
    template_obj = load_template(template=template)
    wiki_item = template_obj.render(ns=ns,
                                    item_dict=item,
                                    item_name=item_name)
    return wiki_item

