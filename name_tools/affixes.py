import re

# I realize *fixes may not be the proper linguistic terms for these.

# No attempt was made to be exhaustive, but some sources used:
# http://en.wikipedia.org/wiki/List_of_post-nominal_letters
# http://en.wikipedia.org/wiki/Pre-nominal_letters
# http://en.wikipedia.org/wiki/Forms_of_address_in_the_United_Kingdom

# Of these, dropping the first 9 are the most likely to cause
# false matches. Perhaps they should be treated separately?
_suffixes = ['Jr', 'Sr', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII',
            'PhD', 'MD', 'DD', 'JD', 'PharmD', 'PsyD', 'RN', 'EngD',
            'DPhil', 'MA', 'MF', 'MBA', 'MSc', 'MEd', 'EdD', 'DMin',
            'AB', 'BA', 'BFA', 'BSc', 'Esq', 'Esquire', 'MP', "MS",
            'USA', 'USAF', 'USMC', 'USCG', 'USN', 'Ret', r'\(Ret\)',
            'CPA', 'Junior', 'Senior']

_prefixes = ['Mr', 'Mister', 'Mrs', 'Ms', 'Miss', 'Dr', 'Doctor',
             'Professor', 'The', 'Honou?rable', 'Chief', 'Justice',
             'His', 'Her', 'Honou?r', 'Mayor', 'Associate', 'Majesty',
             'Judge', 'Master', 'Sen', 'Senator', 'Rep', 'Deputy',
             'Representative', 'Congress(wo)?man', 'Sir', 'Dame',
             'Speaker', r'(Majority|Minority)\W+Leader',
             'President', 'Chair(wo)?man', 'Pres', 'Governor',
             'Gov', 'Assembly\W+Member', 'Highness', 'Hon',
             'Prime\W+Minister', r'P\.?M', 'Admiral', 'Adm',
             'Colonel', 'Col', 'General', 'Gen', 'Captain',
             'Capt', 'Corporal', 'CPL', 'PFC', 'Private',
             r'First\W+Class', 'Sergeant', 'Sgt', 'Commissioner',
             'Lieutenant', 'Lt', 'Lieut', 'Brigadier',
             'Major', 'Maj', 'Officer', 'Pilot',
             'Warrant', 'Officer', 'Cadet', 'Reverand',
             'Minister', 'Venerable', 'Father', 'Mother', 'Brother',
             'Sister', 'Rabbi', 'Fleet']

# The suffixes are obviously not all acronyms but there are probably
# plenty of people out there mistakenly writing things like 'J.r.',
# so we go ahead and allow periods between any letters
_suffix_pattern = [r"\.?".join(suffix) for suffix in _suffixes]
_suffix_pattern = r'\W*,?(\W+(%s)\.?,?)+\W*$' % r"|".join(_suffix_pattern)
_suffix_pattern = re.compile(_suffix_pattern, re.IGNORECASE)

_prefix_pattern = r'^\W*((%s)\.?(\W+|$))+' % r"|".join(_prefixes)
_prefix_pattern = re.compile(_prefix_pattern, re.IGNORECASE)


def drop_affixes(name):
    """
    >>> drop_affixes("Mr. Michael Stephens, Jr.")
    'Michael Stephens'
    >>> drop_affixes("Lieutenant Col. Michael Stephens III, U.S.M.C. (Ret)")
    'Michael Stephens'
    >>> drop_affixes(" His Honour, Mayor M. Stephens III, J.D., M.D., RN ")
    'M. Stephens'
    >>> drop_affixes("Mr. Chief Justice")
    ''
    >>> drop_affixes("Michael Stephens")
    'Michael Stephens'
    >>> drop_affixes(" Michael Stephens ")
    'Michael Stephens'
    >>> drop_affixes(" Stephens, Michael ")
    'Stephens, Michael'
    """
    return split_affixes(name)[1]


def split_affixes(name):
    """
    >>> split_affixes("Mr. Michael Stephens, Jr.")
    ('Mr.', 'Michael Stephens', 'Jr.')
    >>> split_affixes("Lieutenant Col. Michael Stephens III, U.S.M.C. (Ret)")
    ('Lieutenant Col.', 'Michael Stephens', 'III, U.S.M.C. (Ret)')
    >>> split_affixes(" His Honour, Mayor M. Stephens III, J.D., M.D., RN ")
    ('His Honour, Mayor', 'M. Stephens', 'III, J.D., M.D., RN')
    >>> split_affixes("Mr. Chief Justice")
    ('Mr. Chief Justice', '', '')
    >>> split_affixes("Michael Stephens")
    ('', 'Michael Stephens', '')
    >>> split_affixes(" Michael Stephens ")
    ('', 'Michael Stephens', '')
    >>> split_affixes(" Stephens, Michael ")
    ('', 'Stephens, Michael', '')
    """
    prefixes, name = split_prefixes(name)
    name, suffixes = split_suffixes(name)

    return (prefixes, name, suffixes)


def drop_suffixes(name):
    """
    >>> drop_suffixes("Michael Stephens, Ph.D. J.D, USAF (Ret) III Esq")
    'Michael Stephens'
    >>> drop_suffixes("Michael Stephens Jr  C.P.A ")
    'Michael Stephens'
    >>> drop_suffixes("Stephens, Michael Jr.")
    'Stephens, Michael'
    >>> drop_suffixes("Stephens, Michael ")
    'Stephens, Michael'
    >>> drop_suffixes("Stephens, M.")
    'Stephens, M.'
    """
    return split_suffixes(name)[0]


def split_suffixes(name):
    """
    >>> split_suffixes("Michael Stephens, Ph.D. J.D, USAF (Ret) III Esq")
    ('Michael Stephens', 'Ph.D. J.D, USAF (Ret) III Esq')
    >>> split_suffixes("Michael Stephens Jr  C.P.A ")
    ('Michael Stephens', 'Jr  C.P.A')
    >>> split_suffixes("Stephens, Michael Jr.")
    ('Stephens, Michael', 'Jr.')
    >>> split_suffixes("Stephens, Michael ")
    ('Stephens, Michael', '')
    >>> split_suffixes("Stephens, M.")
    ('Stephens, M.', '')
    """
    name = name.rstrip()

    match = _suffix_pattern.search(name)
    if match:
        return (name[0:match.start()].rstrip(),
                match.group().lstrip('., \t\r\n'))

    return (name, '')


def drop_prefixes(name):
    """
    >>> drop_prefixes("Mr. Michael Stephens")
    'Michael Stephens'
    >>> drop_prefixes("Mr Michael Stephens")
    'Michael Stephens'
    >>> drop_prefixes(" Doctor Michael Stephens")
    'Michael Stephens'
    >>> drop_prefixes("The  Honorable Michael Stephens")
    'Michael Stephens'
    >>> drop_prefixes("The Hon Mr. Michael Stephens")
    'Michael Stephens'
    >>> drop_prefixes("  Michael Stephens")
    'Michael Stephens'
    >>> drop_prefixes("M. Stephens")
    'M. Stephens'
    """
    return split_prefixes(name)[1]


def split_prefixes(name):
    """
    >>> split_prefixes("Mr. Michael Stephens")
    ('Mr.', 'Michael Stephens')
    >>> split_prefixes("Mr Michael Stephens")
    ('Mr', 'Michael Stephens')
    >>> split_prefixes(" Doctor Michael Stephens")
    ('Doctor', 'Michael Stephens')
    >>> split_prefixes("The  Honorable Michael Stephens")
    ('The  Honorable', 'Michael Stephens')
    >>> split_prefixes("The Hon Mr. Michael Stephens")
    ('The Hon Mr.', 'Michael Stephens')
    >>> split_prefixes("  Michael Stephens")
    ('', 'Michael Stephens')
    >>> split_prefixes("M. Stephens")
    ('', 'M. Stephens')
    """
    name = name.lstrip()

    match = _prefix_pattern.match(name)
    if match:
        return (match.group(0).strip(),
                name[match.end():len(name)].lstrip())

    return ('', name)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
