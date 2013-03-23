import urllib2


def scrap_subpage(url):
    result = []
    html = urllib2.urlopen(url).read()
    splitted = html.split('\n')
    for line in splitted:
        if line.startswith('<td class="cpt">'):
            cells = line.split('</td>')
            from_row = (
                cells[0].split('>')[1][2:],
                cells[1].split('>')[1],
                cells[2].split('>')[1].lower(),

            )
            if from_row[-1] != "":
                result.append(from_row)
    return result


def to_formatted_str(symbols_list):
    result = '# -*- coding: utf-8 -*-\nsymbols = [\n'
    for symbol in symbols_list:
        result += """["{s[0]}", \"\"\"{s[1]}\"\"\", "{s[2]}"],\n""".format(s=symbols_list)
    result += ']'
    return result


url = 'http://www.utf8-chartable.de/unicode-utf8-table.pl?start={start}&number={step}&utf8=-'


def scrap(start=0, end=120000, step=1024):
    result = []
    while start < end:
        result.extend(scrap_subpage(url.format(start=start, step=step)))
        start += step
    return result

fi = open('symbols.py', 'w')
fi.write(to_formatted_str(scrap()))
fi.close()
