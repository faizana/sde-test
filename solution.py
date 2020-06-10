
import json
import numpy
import re
import sys



def get_valid_bond_objects(json,valid_field_list = ['yield','tenor','type','id']):
    valid_json = json
    valid_json['data'] = list(filter(lambda x: set(valid_field_list).intersection(set([k for k in x.keys() if x[k] is not None])) == set(valid_field_list), json['data']))
    return valid_json


def create_map_for_benchmark(cross_join_bonds):
    benchmark_results = dict()
    for benchmark in cross_join_bonds:
        cid = benchmark[0]['id']
        if cid not in benchmark_results.keys():
            benchmark_results[cid] = []

        corp_tenor = float(re.match(r'([+-]?\d+(?:\.\d+)?)|(\B-\B)',benchmark[0]['tenor']).group())
        govt_tenor = float(re.match(r'([+-]?\d+(?:\.\d+)?)|(\B-\B)',benchmark[1]['tenor']).group())
        term_diff = abs(corp_tenor-govt_tenor)
        corp_yield = float(benchmark[0]['yield'].replace('%',''))
        govt_yield = float(benchmark[1]['yield'].replace('%',''))
        spread = int((corp_yield - govt_yield)*100)
        benchmark_results[cid].append(dict(term_diff = term_diff,
                                           cid = cid, gid = benchmark[1]['id'],
                                           spread = spread))
    return benchmark_results



def get_benchmark(benchmark_results):
    best_results = {k:sorted(v,key=lambda x: x['term_diff'])[0] for k,v in benchmark_results.items()}
    final_output = dict(data = [])
    for k,v in best_results.items():
        bond_match = dict(corporate_bond_id = k,government_bond_id = v['gid'], spread_to_benchmark = "{} bps".format(v['spread']))
        final_output['data'].append(bond_match)
    return final_output



def find_best_benchmark(input_json):
    valid_bonds = get_valid_bond_objects(input_json)
    govt_bonds = list(filter(lambda x: x['type']=='government',valid_bonds['data']))
    corp_bonds = list(filter(lambda x: x['type'] =='corporate',valid_bonds['data']))
    cross_join_bonds = numpy.transpose([numpy.tile(corp_bonds, len(govt_bonds)),
                                numpy.repeat(govt_bonds, len(corp_bonds))])

    benchmark_results = create_map_for_benchmark(cross_join_bonds)

    return get_benchmark(benchmark_results)


def main():
    args = sys.argv

    if(len(sys.argv) == 3):
        input_json = args[1]
        output_json = args[2]
        with open(input_json, 'r') as json_file:
            data = json.load(json_file)
        result = find_best_benchmark(data)
        with open(output_json, 'w') as outfile:
            json.dump(result, outfile)
    else:
        print("Invalid command line args")




if __name__ == '__main__':
    main()




