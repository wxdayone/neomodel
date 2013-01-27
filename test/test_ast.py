from neomodel.queryset import ast, render
from neomodel import OUTGOING


def test_simple_match():
    qast = [
            ast.start_node_id(3),
            ast.match(['self', ast.rel(OUTGOING, 'COUSIN'), 'c']),
            ast.ret(['c'])
        ]
    result = render.tree(qast).replace("\n", ' ')
    assert result == "START self=node(3) MATCH (self)-[r1:COUSIN]->(c) RETURN c"


def test_two_part_path_match():
    qast = [
            ast.start_node_id(3),
            ast.match(['self', ast.rel(OUTGOING, 'FRIEND'), 'c',
                ast.rel(OUTGOING, 'OWNS'), 'screwdriver'
            ]),
            ast.ret(['screwdriver'])
        ]

    result = render.tree(qast)
    assert result == '''START self=node(3)
MATCH (self)-[r1:FRIEND]->(c)-[r2:OWNS]->(screwdriver)
RETURN screwdriver'''


def test_multiple_match():
    qast = [
            ast.start_node_id(3),
            ast.match(['self', ast.rel(OUTGOING, 'FRIEND'), 'c'],
                ['c', ast.rel(OUTGOING, 'OWNS'), 'screwdriver']),
            ast.ret(['c'])
        ]
    result = render.tree(qast)
    assert result == """START self=node(3)
MATCH (self)-[r1:FRIEND]->(c),
(c)-[r2:OWNS]->(screwdriver)
RETURN c"""
