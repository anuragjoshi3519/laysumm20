from os import listdir, mkdir
from os.path import isdir
from networkx import Graph
from networkx.algorithms.approximation import min_weighted_vertex_cover

from utils import get_sentences_with_factors, document_word_count, compute_entailment, compute_threshold, \
    create_edge_set, write_summary


def generate_wMVC_summ(input_path: str, reference_path: str, output_path: str, limit: int):
    for doc in listdir(input_path):
        with open(input_path + doc, 'r') as f:
            txt = f.read()
            if txt == '' or txt == 'None.':
                open(output_path + doc, 'w', encoding='utf8').write('')
                continue

        sent_tokens, factors = get_sentences_with_factors(input_path, reference_path, doc)

        if document_word_count(sent_tokens) < 250:
            open(output_path + doc, 'w', encoding='utf8').write('\n\n'.join(sent_tokens))
            continue

        dist = compute_entailment(sent_tokens)

        threshold = compute_threshold(dist, 0.5)
        large = 2 * max(factors) * len(sent_tokens)

        vertices = [(i, {'weight': large - factors[i] * (sum(dist[i]) - 1)})
                    for i in range(len(sent_tokens))]

        edges = create_edge_set(dist, threshold)

        G = Graph()
        G.add_nodes_from(vertices)
        G.add_edges_from(edges)

        wMVC = min_weighted_vertex_cover(G, 'weight')

        tops = sorted([i for i in wMVC],
                      key=lambda x: vertices[x][1]['weight'])

        write_summary(output_path, doc, limit, sent_tokens, tops)


def generate_wMVC():
    root_path = 'Data/Input-wMVC/'
    for section in listdir(root_path):
        input_path = root_path + section + '/'
        reference_path = input_path
        output_path = f'Data/Input-BART/{section}/'
        if not isdir(output_path):
            mkdir(output_path)

        if section == 'Conclusions':
            generate_wMVC_summ(input_path, reference_path, output_path, 150)
        else:
            generate_wMVC_summ(input_path, reference_path, output_path, 170)
