import re
from affixes import drop_prefixes, drop_suffixes
from itertools import combinations
import string

_funcs = {string.lower: 0.01,
          (lambda s: s.replace('.', '')): 0.02,
          (lambda s: s.replace(',', '')): 0.02,
          drop_prefixes: 0.05,
          drop_suffixes: 0.05,}
# other things to consider:
# Michael Stephens -> Stephens, Michael
# accented characters -> unaccented equiv.
# just last name
# remove consecutive inner spaces (probably no penalty)
# some sort of soundex thing?

_combinations = []
for n in xrange(0, len(_funcs)):
    _combinations.extend(combinations(_funcs.items(), n))

def match(name1, name2):
    """
    >>> match("Michael Stephens", "Michael Stephens")
    1.0
    >>> abs(match("michael stephens", "Michael Stephens") - 0.99) < 0.001
    True
    >>> abs(match("michaeL StepHens", "MichaEl StePhens") - 0.98) < 0.001
    True
    >>> abs(match("Michael J. Stephens", "Michael J Stephens") - 0.98) < 0.001
    True
    >>> abs(match("M. J. Stephens", "M J. Stephens") - 0.96) < 0.001
    True
    >>> abs(match("Michael Stephens", "Mr. Michael Stephens") - 0.95) < 0.001
    True
    >>> abs(match("Mr. Michael Stephens", "Michael Stephens, M.S.") - 0.90) < 0.001
    True
    >>> abs(match("Mr. M. Stephens, Jr.", "Dr. M Stephens, USMC (Ret)") - 0.78) < 0.001
    True
    >>> match("Michael Stephens", "Bob Smith")
    0.0
    >>> match("", " ")
    0.0
    """
    if name1 == name2:
        return 1.0

    if not name1.strip() or not name2.strip():
        return 0.0

    s1 = set()
    s2 = set()
    for combo in _combinations:
        n1, n2 = name1, name2
        penalty = 0.0
        for (func, mod) in combo:
            n1 = func(n1)
            n2 = func(n2)
            penalty += mod
        s1.add((n1, penalty))
        s2.add((n2, penalty))

    max = 0.0
    for p1 in s1:
        for p2 in s2:
            if p1[0] == p2[0]:
                score = 1.0 - p1[1] - p2[1]
                if score > max:
                    max = score

    return max

if __name__ == '__main__':
    import doctest
    doctest.testmod()
