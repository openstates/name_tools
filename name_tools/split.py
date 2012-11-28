import re
from .affixes import split_prefixes, split_suffixes

# List of compound prefixes adapted from
# http://code.google.com/p/php-name-parser/
_compound_prefixes = ['vere', 'von', 'van', 'de', 'del', 'della', 'di', 'da',
                      'pietro', 'vanden', 'du', r'st\.', 'st', 'la', 'ter',
                      'bin']
_compound_pattern = re.compile(r'\b(%s)\b.+$' % r'|'.join(_compound_prefixes),
                               re.IGNORECASE)


def split(name):
    """
    Splits a string containing a name into a tuple of 4 strings,
    (prefixes, first_part, last_part, suffixes), any of which may be empty
    if the name does not include a corresponding part.

      * prefixes is the part of the name consisting of titles that precede
        a name in typical speech ('Mr.', 'Dr.', 'President')
      * first_part corresponds to included given name(s), first initial(s),
        middle name(s) and/or middle initial(s) (e.g. 'Fred', 'F. Scott',
        'Barack Hussein')
      * last_part corresponds to a last name (e.g. 'Smith', 'van Dyke')
      * suffixes corresponds to generational suffixes ('Jr.', 'III', etc.),
        academic suffixes ('Ph.D.', 'M.A.', etc.) and other titles that
        typically follow a name

    This function is geared towards Western-style names with English language
    affixes. While complete accuracy isn't possible, an attempt was made to
    cover a wide variety of commonly occurring name styles.

    Examples:

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
    >>> split("Fleet Admiral Michael J. Stephens, Jr., USN")
    ('Fleet Admiral', 'Michael J.', 'Stephens', 'Jr., USN')
    >>> split("Stephens, President Michael J.")
    ('President', 'Michael J.', 'Stephens', '')
    >>> split("Stephens, Mr. M J III")
    ('Mr.', 'M J', 'Stephens', 'III')
    >>> split("M. Stephens")
    ('', 'M.', 'Stephens', '')
    >>> split("Michael S.")
    ('', 'Michael', 'S.', '')
    >>> split('Michael "Mike" Stephens')
    ('', 'Michael "Mike"', 'Stephens', '')
    >>> split('Stephens Jr., Michael')
    ('', 'Michael', 'Stephens', 'Jr.')
    >>> split('His Honour, Mayor Michael J. Stephens')
    ('His Honour, Mayor', 'Michael J.', 'Stephens', '')
    >>> split('Major Stephens')
    ('', 'Major', 'Stephens', '')
    >>> split('Stephens, Major')
    ('', 'Major', 'Stephens', '')
    >>> split('Van Stephens')
    ('', 'Van', 'Stephens', '')
    >>> split('Representative Justice')
    ('Representative', '', 'Justice', '')
    """
    name_ns, suffixes = split_suffixes(name)
    i = name_ns.find(', ')

    # Last part first
    if i != -1:
        last_part, first_part = name_ns.split(', ', 1)
        last_part, more_suffixes = split_suffixes(last_part)
        if more_suffixes:
            if suffixes:
                suffixes += " "
            suffixes += more_suffixes

        prefixes, first_part = split_prefixes(first_part)
        if prefixes and not first_part and ' ' not in prefixes:
            first_part = prefixes
            prefixes = ''

        first_part = first_part.strip()
        last_part = last_part.strip()

        # We check that first and last are not empty, and that
        # last is not just prefixes (in which case we probably
        # misinterpreted a prefix with a comma for a last name),
        # skipping on to the other name splitting algorithm
        # if true.
        if last_part and first_part and split_prefixes(last_part)[1]:
            return (prefixes, first_part, last_part, suffixes)

    # First part first

    # Look for compound last name
    prefixes, name_na = split_prefixes(name_ns)
    m = _compound_pattern.search(name_na)
    if m and m.start() != 0:
        first_part = name_na[0:m.start()]
        last_part = m.group(0)
    else:
        words = name_na.split()
        first_part = ' '.join(words[0:-1])
        if not words:
            last_part = ''
        else:
            last_part = words[-1]

    first_part = first_part.strip()
    last_part = last_part.strip()

    # Some 'prefixes' can also be first names (e.g. 'Major'). If
    # we found one prefix and no first name, swap them.
    if prefixes and not first_part and ' ' not in prefixes:
        first_part = prefixes
        prefixes = ''

    # Sometimes a last name looks like a prefix. If we found
    # prefixes but no last name, the last prefix is probably
    # actually the last name
    if prefixes and not last_part:
        pre_words = prefixes.split()
        last_part = pre_words[-1]
        prefixes = ' '.join(pre_words[0:-1])

    return (prefixes, first_part, last_part, suffixes)


_namecase = {'ii': 'II', 'iii': 'III', 'iv': 'IV', 'vi': 'VI', 'vii': 'vii'}


def namecase(name):
    """
    >>> namecase('michael stephens')
    'Michael Stephens'
    >>> namecase('m. stephens')
    'M. Stephens'
    >>> namecase('m.j. stephens')
    'M.J. Stephens'
    >>> namecase('Michael Stephens, iii')
    'Michael Stephens, III'
    >>> namecase("michael o'stephens")
    "Michael O'Stephens"
    """
    return re.sub(r"[A-Za-z]+('[A-Za-z]+])?",
                  lambda mo: _namecase.get(mo.group(0).lower(),
                                           mo.group(0).title()),
                  name)


def canonicalize(name):
    """
    >>> canonicalize('  stephens, michael jr.')
    'Michael Stephens, Jr.'
    >>> canonicalize('MICHAEL, JR.')
    'Michael, Jr.'
    >>> canonicalize('Father Michael X. y. stephens, III, u.s.c.g.')
    'Father Michael X. Y. Stephens, III, U.S.C.G.'
    """
    prefixes, first_part, last_part, suffixes = split(name)
    canonical = ""
    if prefixes:
        canonical = namecase(prefixes)
    if first_part:
        canonical += " " + namecase(first_part)
    if last_part:
        canonical += " " + namecase(last_part)
    if suffixes:
        canonical += ", " + namecase(suffixes)
    return canonical.strip()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
