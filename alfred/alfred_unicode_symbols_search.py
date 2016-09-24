from alfred import AlfredItemsList
from unicode_symbols_search import search_symbols


import sys
query_text = ' '.join(sys.argv[1:])


al = AlfredItemsList()
icon = 'icon'
for symbol, description in search_symbols(query_text):
    codepoints = symbol.encode(
        "unicode_escape"
    ).decode('utf-8').replace('\\u', ' ').replace('\\U', ' ').strip()
    al.append(symbol, symbol, codepoints + ' | ' + description, icon=icon)
    icon = 'noicon'

print(al)
