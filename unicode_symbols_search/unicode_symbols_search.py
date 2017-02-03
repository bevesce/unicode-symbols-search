import os


def search_symbols(query_text, symbols=None):
    if not symbols:
        symbols = load_symbols()
    query = create_query(query_text)
    for symbol in symbols:
        if query(symbol):
            yield symbol


def create_query(query_text):
    query_words = query_text.split(' ')

    def is_symbol_matching(symbol):
        symbol_itself, description = symbol
        symbol_matches = symbol_itself == query_text
        description_matches = all(word in description for word in query_words)
        return symbol_matches or description_matches
    return is_symbol_matching


def load_symbols(path=None):
    if not path:
        path = get_symbols_path()
    return [parse_symbol(l) for l in read6(path).splitlines()]


def parse_symbol(line):
    split = line.split('| ')
    return split[0].strip(), split[1]


def get_symbols_path():
    return os.path.join(os.path.split(__file__)[0], 'symbols.txt')


def read6(path):
    try:
        with open(path, encoding='utf-8') as f:
            return f.read()
    except:
        with open(path) as f:
            return f.read().decode('utf-8')


if __name__ == '__main__':
    import sys
    query_text = ' '.join(sys.argv[1:])
    for symbol, description in search_symbols(query_text):
        print(symbol + '\t' + description)
