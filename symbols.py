# -*- coding: utf-8 -*-
#!/usr/bin/python


from symbols_list import symbols
from alfredlist import AlfredItemsList


def prepare_query(query):
    return query.strip().lower().split(' ')


def matches(query, description):
    return all(q in description for q in query)


def filter_symbols(query=''):
    query = prepare_query(query)
    result = []
    for idx, symbol in enumerate(symbols):
        hex_string, symbol, description = symbol
        if matches(query, description):
            result.append((hex_string, symbol, description, idx))
    return result


def unpack_if_list(hex_string):
    if isinstance(hex_string, list):
        hex_string = hex_string[0]
    return hex_string


def to_html(hex_string):
    hex_string = unpack_if_list(hex_string)
    return '&#x' + str(hex_string) + ';'


def to_symbol(hex_string):
    # return '-?-'
    hex_string = unpack_if_list(hex_string)
    as_int = int(hex_string, 16)
    if as_int >= 65536:
        return '-?-'
    return unichr(as_int).encode('utf-8')


def to_python(hex_string):
    hex_string = unpack_if_list(hex_string)
    return 'u"\\u' + hex_string + '"'


def to_codepoint(hex_string):
    hex_string = unpack_if_list(hex_string)
    return 'U+' + hex_string


def get_by_idx(idx):
    return symbols[int(idx)]


def alfred_xml(query):
    symbols_list = filter_symbols(query)
    al = AlfredItemsList()
    for hex_string, symbol, description, idx in symbols_list:
        al.append(
            arg=idx,
            title=' ' + symbol,
            subtitle=description,
            uid='utf_symbols' + str(idx)
        )
    return al


def present(symbols):
    print 'symbol   codepoint   html   python   description'
    print '------------------------------------------------'
    for symbol in symbols:
        hex_string = symbol[0]
        symbol_char = symbol[1]
        description = symbol[2]
        print symbol_char + '  ' +\
            to_codepoint(hex_string) + '  ' +\
            to_html(hex_string) + '  ' +\
            to_python(hex_string) + '  ' +\
            description


if __name__ == "__main__":
    import sys
    query = ''
    if len(sys.argv) > 1:
        if sys.argv[1] == '-a':
            query = ' '.join(sys.argv[2:])
            print alfred_xml(query).to_ustr().encode('utf-8')
        else:
            query = ' '.join(sys.argv[2:])
            present(filter_symbols(query))
