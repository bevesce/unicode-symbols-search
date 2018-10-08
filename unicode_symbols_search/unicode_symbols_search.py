import os


def search_symbols(query_text, symbols=None):
    if not symbols:
        symbols = get_symbols()
    query = create_query(query_text)
    for symbol in symbols:
        if query(symbol):
            yield symbol


def create_query(query_text):
    query_words = query_text.split(' ')
    letters = [l for l in query_words if len(l) == 1]
    if len(letters) == 1:
        return create_single_letter_query(letters[0], query_words)
    return create_words_query(query_words)


def create_single_letter_query(letter, query_words):
    words_query = create_words_query(query_words)
    prefix = letter + ' '
    sufix = ' ' + letter
    infix = ' ' + letter + ' '

    def is_letter_in_symbol(symbol):
        symbol_itself, description, _ = symbol
        return (
            symbol_itself == letter or
            description.startswith(prefix) or
            description.endswith(sufix) or
            infix in description
        ) and words_query(symbol)
    return is_letter_in_symbol


def create_words_query(query_words):
    def is_symbol_matching(symbol):
        symbol_itself, description, hidden_description = symbol
        symbol_matches = symbol_itself in query_words
        full_description = description + ' ' + hidden_description
        description_matches = all(
            word in full_description for word in query_words
        )
        return symbol_matches or description_matches
    return is_symbol_matching



symbols = None

def get_symbols(path=None):
    global symbols
    if not symbols:
        if not path:
            path = get_symbols_path()
        symbols = [parse_symbol(l) for l in read6(path).splitlines()]
    return symbols


def parse_symbol(line):
    split = line.split('| ')
    symbol = split[0][1:]
    description = (' '.join(split[1:]).lower()).split('# ')
    main_description = description[0]
    hidden_description = ' '.join(description[1:])
    return symbol, main_description, hidden_description


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
    for symbol, description, _ in search_symbols(query_text):
        print(symbol + '\t' + description)
