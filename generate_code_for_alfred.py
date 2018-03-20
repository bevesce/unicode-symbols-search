alfred_code = """
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cgi import escape
from uuid import uuid4
import os
import sys


class AlfredItemsList(object):
    def __init__(self, items=None):
        self.items = items or []
        self.pattern = (
            '<item arg="{arg}" uid="{uid}" valid="{valid}">"' +
                '<title>{title}</title>' +
                '<subtitle>{subtitle}</subtitle>' +
                '<icon>no-icon</icon>'
            '</item>'
        )

    def append(
        self, arg, title, subtitle,
        valid='yes', uid=None
    ):
        uid = uid or str(uuid4())
        self.items.append(
            (arg, escape(title), escape(subtitle), valid, uid)
        )

    def __str__(self):
        items = "".join([
            self.pattern.format(
                arg=arg,
                title=escape(title),
                subtitle=escape(subtitle),
                valid=valid,
                uid=uid
            ) for arg, title, subtitle, valid, uid in self.items
        ])
        return ('<items>' + items + '</items>').encode('utf-8')

    def __add__(self, other):
        return AlfredItemsList(self.items + other.items)
"""

with open('./unicode_symbols_search/unicode_symbols_search.py') as f:
    unicode_symbols_search_code = f.read()


from unicode_symbols_search import get_symbols

unicode_symbols_search_code = unicode_symbols_search_code.replace(
    'symbols = None',
    'symbols = {}'.format(get_symbols())
).split("if __name__ == '__main__':")[0]

execute_code = """
query_text = ' '.join(sys.argv[1:])
al = AlfredItemsList()
for symbol, description, _ in search_symbols(query_text):
    escaped = symbol.encode('unicode_escape')
    codepoints = escaped.replace('\\\\u', ' ').replace('\\\\U', ' ').strip()
    al.append(symbol, symbol, description + ' | ' + codepoints, uid=symbol)

print(al)
"""

code = '\n\n'.join([
    alfred_code,
    unicode_symbols_search_code,
    execute_code,
])
print(code)
