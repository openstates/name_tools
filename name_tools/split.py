from affixes import split_prefixes, split_suffixes
import re

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
    """
    name_ns, suffixes = split_suffixes(name)
    i = name_ns.find(', ')
    if i != -1:
        last_part, first_part = name_ns.split(', ', 1)
        prefixes, first_part = split_prefixes(first_part)
    else:
        # Look for compound last name
        prefixes, name_na = split_prefixes(name_ns)
        m = _compound_pattern.search(name_na)
        if m:
            first_part = name_na[0:m.start()]
            last_part = m.group(0)
        else:
            words = name_na.split()
            first_part = ' '.join(words[0:-1])
            last_part = words[-1]

    return (prefixes, first_part.strip(), last_part.strip(), suffixes)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
