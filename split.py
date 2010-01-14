from affixes import split_affixes
import re

# List of compound prefixes adapted from
# http://code.google.com/p/php-name-parser/
_compound_prefixes = ['vere', 'von', 'van', 'de', 'del', 'della', 'di', 'da', 
                      'pietro', 'vanden', 'du', r'st\.', 'st', 'la', 'ter']
_compound_pattern = re.compile(r'\b(%s)\b.+$' % r'|'.join(_compound_prefixes),
                               re.IGNORECASE)

def split(name):
    """
    >>> split("Michael Stephens")
    ('', 'Michael', 'Stephens', '')
    >>> split("Stephens, Michael")
    ('', 'Michael', 'Stephens', '')
    >>> split("Michael von Stephens")
    ('', 'Michael', 'von Stephens', '')
    >>> split("Michael J. Stephens")
    ('', 'Michael J.', 'Stephens', '')
    >>> split("Mr. Michael Joseph de la Stephens, III, C.P.A.")
    ('Mr.', 'Michael Joseph', 'de la Stephens', 'III, C.P.A.')
    """
    # TODO: return affixes instead of just dropping them
    prefixes, name, suffixes = split_affixes(name)
    i = name.find(', ')
    if i != -1:
        last_part, first_part = name.split(', ')
    else:
        # Look for compound last name
        m = _compound_pattern.search(name)
        if m:
            first_part = name[0:m.start()]
            last_part = m.group(0)
        else:
            split_name = name.split()
            first_part = ' '.join(split_name[0:-1])
            last_part = split_name[-1]

    return (prefixes, first_part.strip(), last_part.strip(), suffixes)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
