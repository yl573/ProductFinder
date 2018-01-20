# currently finds the first product with a name or alias containing the search_name
def fuzzy_match(search_name, products):
    match = []
    for product in products:
        if (search_name.lower() in product['Name'].lower()
            or search_name.lower() in product['Alias'].lower()):
            match.append(product)
    return match