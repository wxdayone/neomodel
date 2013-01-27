from py2neo.neo4j import Direction
OUTGOING = Direction.OUTGOING
INCOMING = Direction.INCOMING
EITHER = Direction.EITHER


def start(clause):
    if isinstance(clause['node'], (dict,)):
        return "START {as}=node:{index}({query})".format(**clause)
    else:
        return "START {as}=node({node})".format(**clause)


def rel(rel):
    if rel['direction'] == OUTGOING:
        stmt = '-[{as}:{type}]->'
    elif rel['direction'] == INCOMING:
        stmt = '<-[{as}:{type}]-'
    elif rel['direction'] == EITHER:
        stmt = '-[{as}:{type}]-'
    return stmt.format(**rel)


def match(stmt):
    output = ''
    for pattern in stmt:
        output += ",\n" if len(output) else ''
        for index, part in enumerate(pattern):
            output += rel(part) if index % 2 else '({0})'.format(part)
    return "MATCH " + output


def ret(parts):
    return 'RETURN ' + ', '.join([
        "{0}.{1}".format(*p) if isinstance(p, (tuple,)) else str(p)
                for p in parts])


def tree(ast):
    query = ''
    for keyword, clause in ast:
        if 'start' is keyword:
            query += start(clause) + "\n"
        elif 'match' is keyword:
            query += match(clause) + "\n"
        elif 'return' is keyword:
            query += ret(clause)
    return query
