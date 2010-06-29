import name_tools


def forms(name):
    """
    >>> forms = name_forms("Michael Stephens")
    >>> 'michael stehpens' in forms
    True
    >>> 'stephens, michael' in forms
    True
    >>> 'm stephens' in forms
    True
    >>> 'stephens' in forms
    True
    """
    sname = {}
    (sname['pre'], sname['first'],
     sname['last'], sname['post']) = name_tools.split(name)

    forms = set()

    def add_form(str):
        str = (str % sname).strip(', \t\r\n').lower()
        str = str.replace('.', '')

        # Collapse all whitespace segments into single space characters
        str = ' '.join(str.split())

        forms.add(str)

    add_form("%(first)s %(last)s")
    add_form("%(last)s")
    add_form("%(pre)s %(first)s %(last)s")
    add_form("%(first)s %(last)s %(post)s")
    add_form("%(pre)s %(first)s %(last)s")
    add_form("%(pre)s %(first)s %(last)s %(post)s")
    add_form("%(last)s, %(first)s")

    pre_first = ("%(pre)s %(first)s" % sname).strip(', \t\r\n')
    add_form("%(last)s, " + pre_first)

    add_form("%s %s" % (sname['first'][0], sname['last']))
    add_form("%s. %s" % (sname['first'][0], sname['last']))

    initials = ' '.join([w[0] for w in sname['first'].split()])

    add_form(initials + " %(last)s")

    add_form("%(last)s, " + initials)

    return forms
