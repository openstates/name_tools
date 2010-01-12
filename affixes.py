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
            'USA', 'USAF', 'USMC', 'USCG', 'Ret', r'\(Ret\)',
            'CPA',]

_prefixes = ['Mr', 'Mister', 'Mrs', 'Ms', 'Miss', 'Dr', 'Doctor',
             'Professor', 'The', 'Honou?rable', 'Chief', 'Justice',
             'His', 'Her', 'Honou?r', 'Mayor', 'Associate', 'Majesty',
             'Judge', 'Master', 'Sen', 'Senator', 'Rep', 'Deputy',
             'Representative', 'Congress(wo)?man', 'Sir', 'Dame',
             'Speaker', r'(Majority|Minority)\W+Leader',
             'President', 'Chair(wo)?man', 'Pres', 'Governor',
             'Gov', 'Assembly\W+Member', 'Highness', 'Hon',
             'Prime\W+Minister', r'P\.?M', 'Admiral', 'Adm',
             'Colonel', 'Col', 'General', 'Gen',  'Captain',
             'Capt', 'Corporal', 'CPL', 'PFC', 'Private',
             r'First\W+Class', 'Sergeant', 'Sgt', 'Commissioner',
             'Lieutenant', 'Lt', 'Lieut', 'Brigadier',
             'Major', 'Maj', 'Officer', 'Pilot',
             'Warrant', 'Officer', 'Cadet', 'Reverand',
             'Minister', 'Venerable', 'Father', 'Mother', 'Brother',
             'Sister', 'Rabbi',]

# The suffixes are obviously not all acronyms but there are probably
# plenty of people out there mistakenly writing things like 'J.r.',
# so we go ahead and allow periods between any letters
_suffix_pattern = [r"\.?".join(suffix) for suffix in _suffixes]
_suffix_pattern = r'\W*,?\W+(%s)\.?,?\W*$' % r"|".join(_suffix_pattern)
_suffix_pattern = re.compile(_suffix_pattern, re.IGNORECASE)

_prefix_pattern = r'^\W*(%s)\.?(\W+|$)' % r"|".join(_prefixes)
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
    return drop_prefixes(drop_suffixes(name))

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
    # We'll count trailing spaces as a suffix
    name = name.rstrip()

    (name, count) = _suffix_pattern.subn('', name, 1)
    while count > 0:
        (name, count) = _suffix_pattern.subn('', name, 1)

    return name

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
    name = name.lstrip()

    (name, count) = _prefix_pattern.subn('', name, 1)
    while count > 0:
        (name, count) = _prefix_pattern.subn('', name, 1)

    return name

if __name__ == '__main__':
    import doctest
    doctest.testmod()
