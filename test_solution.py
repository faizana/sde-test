
import solution
import numpy

def test_Solution_FilterValidBondObjects_ValidBondObjectsOutput():
    objs = dict(data = [
        {
            "id": "c1",
            "type": "corporate",
            "tenor": "10.3 years",
            "yield": "5.30%",
            "amount_outstanding": 1200000
        },
        {
            "id": "g1",
            "type": "government",
            "tenor": "9.4 years",
            "yield": "3.70%",
            "amount_outstanding": None
        },
        {
            "id": "g2",
            "type": None,
            "tenor": "12.0 years",
            "yield": "4.80%",
            "amount_outstanding": 1750000
        },
        {
            "id": "g4",
            "type": "corporate",
            "tenor": "12.0 years",
            "yield": "4.80%",
            "amount_outstanding": 1250000
        }
    ])
    output = solution.get_valid_bond_objects(objs)


    assert len(output['data']) == 3
    assert(list(map(lambda x: x['id'],output['data'])) == ['c1','g1','g4'])


def test_create_benchmark_map_produces_correct_map():
    corp_bonds = [{
        "id": "c1",
        "type": "corporate",
        "tenor": "10.3 years",
        "yield": "5.30%",
        "amount_outstanding": 1200000
    },{
        "id": "c2",
        "type": "corporate",
        "tenor": "14.3 years",
        "yield": "8.30%",
        "amount_outstanding": 1200000
    }]
    govt_bonds = [{
        "id": "g1",
        "type": "govt",
        "tenor": "12.3 y",
        "yield": "3.30%",
        "amount_outstanding": 1200000
    },{
        "id": "g2",
        "type": "govt",
        "tenor": "11.3 yrs",
        "yield": "1.30%",
        "amount_outstanding": 1200000
    }]

    cross_join_bonds = numpy.transpose([numpy.tile(corp_bonds, len(govt_bonds)),
                                        numpy.repeat(govt_bonds, len(corp_bonds))])
    mapped_output = solution.create_map_for_benchmark(cross_join_bonds)

    assert(mapped_output) == {'c1': [{'term_diff': 2.0, 'cid': 'c1', 'gid': 'g1', 'spread': 200},
                                     {'term_diff': 1.0, 'cid': 'c1', 'gid': 'g2', 'spread': 400}],
                              'c2': [{'term_diff': 2.0, 'cid': 'c2', 'gid': 'g1', 'spread': 500},
                                     {'term_diff': 3.0, 'cid': 'c2', 'gid': 'g2', 'spread': 700}]}

def test_find_best_benchmark():
    benchmarked_map = {'c1': [{'term_diff': 3.0, 'cid': 'c1', 'gid': 'g1', 'spread': 150},
                              {'term_diff': 0.8, 'cid': 'c1', 'gid': 'g2', 'spread': 400}],
                       'c2': [{'term_diff': 1.2, 'cid': 'c2', 'gid': 'g1', 'spread': 80},
                              {'term_diff': 3.5, 'cid': 'c2', 'gid': 'g2', 'spread': 90}]}

    best_benchmark = solution.get_benchmark(benchmarked_map)

    assert best_benchmark == {'data': [{'corporate_bond_id': 'c1',
                                        'government_bond_id': 'g2',
                                        'spread_to_benchmark': '400 bps'},
                                       {'corporate_bond_id': 'c2',
                                        'government_bond_id': 'g1',
                                        'spread_to_benchmark': '80 bps'}]}



