from typing import ClassVar, List, Tuple
from datetime import datetime
from mwclient import Site


def read(page: str) -> Tuple:
    page = site.pages[page]
    if page.exists:
        return page.text(), page.last_rev_time
    else:
        return None, None


def edit(page: str, content: str, summary='', append=False, newpageonly=False):
    page = site.pages[page]
    if page.can('edit'):
        if newpageonly is True and page.exists:
            # def does nothing if only new pages can be written
            # and page already exists
            return False
        if page.text():
            if append is True:
                content += '\n\n' + page.text()  # append to existing text
            page.edit(text=content, summary=summary)
        else:
            page.edit(text=content, summary=summary)
        return True
    else:
        return False


def unpack_ask_response(response):
    # printout is ordered dict
    # TODO: review code
    d = {}
    # import pdb; pdb.set_trace()
    printouts = response['printouts']
    page = response['fulltext']
    d['page'] = page
    for prop in printouts:
        p_item = response['printouts'][prop]
        for prop_val in p_item:
            if isinstance(prop_val, dict) is False:
                d[prop] = prop_val
            else:
                # if len(prop_val) > 0:
                props = list(prop_val.keys())
                if 'fulltext' in props:
                    val = prop_val.get('fulltext')
                elif 'timestamp' in props:
                    val = datetime.fromtimestamp(
                        int(prop_val.get('timestamp')))
                else:
                    val = list(prop_val.values())[0]
                d[prop] = val
    return(d)


def ask(query: str) -> List:
    results_ = []
    for answer in site.ask(query):
        printouts_dict = unpack_ask_response(answer)
        results_.append(printouts_dict)
    return results_


def login(host: str, path: str, scheme: str, username='', password='') -> \
        ClassVar:
    '''
    Logs in to wiki. Creates the global var site (instance of mwclient.Site),
    though which writing to the wiki is possible
    '''
    site_ = Site(host=host, path=path, scheme=scheme)
    if username and password:
        site_.login(username=username, password=password)
    global site
    site = site_
    return site_

# def create_mw_site(details):
#     site = login(host=details['host'],
#                  path=details['path'],
#                  scheme=details['scheme'],
#                  username=details['username'],
#                  password=details['password'])
