
from difflib import SequenceMatcher

string1 = "apple pie available"
string2 = "come have some apple pies"


def fuzzy_match(search_name, products):
    match = []
    for product in products:
        search = search_name.lower()
        # alias = product['Alias'].lower()
        name = product['Name'].lower()
        common = SequenceMatcher(None, name, search).find_longest_match(0, len(name), 0, len(search))
        if common.size > 4:
            match.append(product)
    return match
