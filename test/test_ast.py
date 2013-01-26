from neomodel import ast, StructuredNode, StringProperty, RelationshipTo


class Badger(StructuredNode):
    name = StringProperty()
    cousins = RelationshipTo('Badger', 'COUSIN')


def test_statement():
    node = Badger(name='greg').save()

    from pprint import pprint as pp
    pp([
        ast.start_point(node),
        ast.build_match(['self', ast.rel('<', 'COUSIN'), 'c']),
        ast.build_return(['c'])
        ])
