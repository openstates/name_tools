import re
from affixes import drop_prefixes, drop_suffixes
from split import split
from itertools import combinations
import string


def initial_initial(name):
    pre, fp, lp, suff = split(name)
    if fp:
        fp = fp[0]
    return " ".join([p for p in [pre, fp, lp, suff] if p])


def middle_initials(name):
    parts = name.split(' ')
    name = parts[0]
    for part in parts[1:-1]:
        name += " " + part[0]
    if len(parts) > 1:
        name += " " + parts[-1]
    return name


def last_only(name):
    return split(name)[2]


def first_first(name):
    parts = split(name)
    return " ".join([p for p in parts if p])


def last_first(name):
    pre, fp, lp, suf = split(name)
    if lp:
        lp += ", "
    return lp + " ".join([p for p in [pre, fp, suf] if p])


_funcs = {string.lower: 0.01,
          (lambda s: s.replace('.', '')): 0.02,
          (lambda s: s.replace(',', '')): 0.02,
          initial_initial: 0.10,
          middle_initials: 0.10,
          drop_prefixes: 0.05,
          drop_suffixes: 0.05,
          first_first: 0.02,
          last_first: 0.02,
          last_only: 0.20}

_combinations = []
for n in xrange(0, len(_funcs)):
    _combinations.extend(combinations(_funcs.items(), n))


def match(name1, name2):
    """
    Provide a measure of the similarity between two name, considering factors
    such as differing word order ('Bond, James' and 'James Bond'), use of
    initials ('J. R. R. Tolkien' and 'John Ronal Reuel Tolkien') and
    various titles and honorifics ('Fleet Admiral William Frederick Halsey,
    Jr., USN', and 'William Frederick Halsey').

    >>> match("Michael Stephens", "Michael Stephens")
    1.0
    >>> abs(match("michael stephens", "Michael Stephens") - 0.99) < 0.001
    True
    >>> abs(match("michaeL StepHens", "MichaEl StePhens") - 0.98) < 0.001
    True
    >>> abs(match("Michael J. Stephens", "Michael J Stephens") - 0.98) < 0.001
    True
    >>> abs(match("Michael Stephens", "Mr. Michael Stephens") - 0.95) < 0.001
    True
    >>> abs(match("Mr. Michael Stephens", "Michael Stephens, M.S.") - 0.90) < 0.001
    True
    >>> abs(match("Mr. M. Stephens, Jr.", "Dr. M Stephens, USMC (Ret)") - 0.78) < 0.001
    True
    >>> abs(match("Michael Joseph Stephens", "Michael J Stephens") - 0.90) < 0.001
    True
    >>> abs(match("M Stephens", "Michael Stephens") - 0.90) < 0.001
    True
    >>> abs(match("Michael Stephens", "Stephens") - 0.80) < 0.001
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
