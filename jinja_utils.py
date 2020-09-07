from jinja2 import (FileSystemLoader,
                    Environment,
                    environment)
from typing import Dict, List, Union, Optional
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


def render_template(template: str, ns: str, item: Union[Dict, List],
                    item_name: Optional[str], page_info: Optional[Dict]) -> str:
    environment.DEFAULT_FILTERS['urlfragment'] = urlfragment
    template_obj = load_template(template=template)
    wiki_item = template_obj.render(ns=ns,
                                    item=item,
                                    item_name=item_name,
                                    page_info=page_info)
    return wiki_item

