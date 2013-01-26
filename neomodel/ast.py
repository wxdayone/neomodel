
"""
Start by index
{'start': {'node': {'index': 'Person', 'query': 'name:Jim'}}},

Start by node
{'start': {'node': 23, 'as': 'self'}},


[
    {'start': {'node': 23, 'as': 'self'}},
    {'match': [['self', {'direction': '<', 'type': 'OWNS', 'as': 'r1'}, 'y']]},
    {'return': [{'identifier': 'y', 'property': 'name'}]}
]
"""


class InvalidMatchPart(TypeError):
    pass


class InvalidMatchSequence(TypeError):
    pass


def start_point(obj, alias='self'):
    return {'start': {'node': obj.__node__.id, 'as': alias}}


def ident_list(identifier, *properties):
    return [{identifier: p}
            for p in properties] if properties else [identifier]


def build_return(items):
    return {'return': items}


def rel(direction=None, rel_type=None, alias=None):
    item = {'direction': direction, 'as': alias}
    if rel_type:
        item['type'] = rel_type
    return item


def build_match(*statements):
    """
        Takes a list of match statements e.g:

        build_match(
            ['a', {'direction': OUTGOING, 'type': 'MOTHER'}, 'b'],
            ['b', {'direction': INCOMING, 'type': 'SISTER'}, 'c'],
        )

        the following get embedded in a match dict
    """
    identifiers = {}
    for match_stmt in statements:
        last_seen = None
        for part in match_stmt:
            if isinstance(part, (basestring,)):
                current = 'identifier'
                identifiers[part] = True
            elif isinstance(part, (dict,)) and 'direction' in part:
                current = 'relation'
            else:
                raise InvalidMatchPart(part)
            if current == last_seen:
                raise InvalidMatchSequence(match_stmt)
            last_seen = current
    return  {'match': statements, '__identifiers__': identifiers}
