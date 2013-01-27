"""
Start by index::
    ('start', {'node': {'index': 'Person', 'query': 'name:Jim'}},)

Start by node::
    ('start', {'node': 23, 'as': 'self'},)

Return nodes connected via incomming OWNS relationship::

    [
        ('start', {'node': 23, 'as': 'self'},),
        ('match', [['self', {'direction': INCOMING, 'type': 'OWNS', 'as': 'r1'}, 'y']],),
        ('return', ['r1', 'y', ('y', 'date')],)
    ]
"""


class InvalidMatchPart(TypeError):
    pass


class InvalidMatchSequence(TypeError):
    pass


def start_node_id(node_id, alias='self'):
    return ('start', {'node': node_id, 'as': alias},)


def property_list(identifier, *properties):
    """
    List of properties to be used in a return or with statement::
        property_list('person', 'name', 'age')
    Returns::
        [('person': 'name',), ('person', 'age',)]
    """
    return [(identifier, p,) for p in properties]


def ident_generator(prefix):
    if not prefix in ident_generator.counter:
        ident_generator.counter[prefix] = 1
        return prefix + str(1)
    else:
        ident_generator.counter[prefix] += 1
        return prefix + str(ident_generator.counter[prefix])
ident_generator.counter = {}


def ret(items):
    """
    Example input::
        [{'person': 'name'}, {'person', 'age'}, 'school']
    Output::
        {'return': [{'person': 'name'}, {'person', 'age'}, 'school']}
    """
    ident_generator.counter = {}
    assert isinstance(items, (list,))
    return ('return', items,)


def rel(direction=None, rel_type=None, alias=None):
    if not alias:
        alias = ident_generator('r')
    item = {'direction': direction, 'as': alias}
    if rel_type:
        item['type'] = rel_type
    return item


def match(*statements):
    """
        Takes a list of match statements e.g:

        build_match(
            ['a', {'direction': OUTGOING, 'type': 'MOTHER'}, 'b'],
            ['b', {'direction': INCOMING, 'type': 'SISTER'}, 'c'],
        )

        the following get embedded in a match dict
    """
    for match_stmt in statements:
        last_seen = None
        for part in match_stmt:
            if isinstance(part, (basestring,)):
                current = 'identifier'
            elif isinstance(part, (dict,)) and 'direction' in part:
                current = 'relation'
            else:
                raise InvalidMatchPart(part)
            if current == last_seen:
                raise InvalidMatchSequence(match_stmt)
            last_seen = current
    return  ('match', statements)
