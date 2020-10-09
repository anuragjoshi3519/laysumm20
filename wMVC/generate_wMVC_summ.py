import os
from os import listdir, mkdir
from os.path import isdir
from nltk.corpus import stopwords
from numpy import array, ndarray, quantile
from nltk.tokenize import word_tokenize, sent_tokenize
from networkx import Graph
from networkx.algorithms.approximation import min_weighted_vertex_cover
from math import log
from regex import sub, I

import nltk
nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))

def write_summary(tops, sent_tokens, limit, document, write_to_path):
    summary_indices1 = []
    count1 = 0
    for sentence in tops:
        cur_len = len(sent_tokens[sentence[0]].split())
        if count1 + cur_len > limit:
            break
        count1 += cur_len
        summary_indices1.append(sentence[0])

    summary1 = []
    for index in sorted(summary_indices1):
        summary1.append(sent_tokens[index])

    summary_indices2 = []
    count2 = 0
    for sentence in tops:
        if count2 >= limit:
            break
        count2 += len(sent_tokens[sentence[0]].split())
        summary_indices2.append(sentence[0])

    summary2 = []
    for index in sorted(summary_indices2):
        summary2.append(sent_tokens[index])

    summary = ''
    if abs(limit - count1) < abs(limit - count2):
        summary += '\n\n'.join(summary1)
    else:
        summary += '\n\n'.join(summary2)

    open(write_to_path + document, 'w', encoding='utf8').write(summary)


def compute_occurrences(sentences):
    filtered = []

    all_tokens = set()
    for sent in sentences:
        filtered.append(set())
        word_tokens = word_tokenize(sent)
        for w in word_tokens:
            if w.lower() not in stop_words:
                filtered[-1].add(w.lower())
                all_tokens.add(w.lower())

    word_occurrence = {}
    for w in all_tokens:
        word_occurrence.update({w: 0})

    for chosen_words in filtered:
        for w in all_tokens:
            if w in chosen_words:
                word_occurrence[w] += 1

    return word_occurrence, filtered


def get_tokens(document):
    result = []
    for sent in [s.strip() for s in document.split('\n') if len(s.strip()) > 0]:
        for puts in sent_tokenize(sent):
            result.append(puts)
    return result


def get_sentences_with_factors(input_path,reference_path,document):
    cur_doc = open(input_path + document, 'r', encoding='utf8').read()
    ref_doc = open(reference_path + document, 'r', encoding='utf8').read()

    cur_doc = sub(r' +', ' ', cur_doc, flags=I)
    ref_doc = sub(r' +', ' ', ref_doc, flags=I)

    summary_sentences = get_tokens(cur_doc)
    summary_sentences_set = set(summary_sentences)

    original_sentences = get_tokens(ref_doc)
    original_sentences_set = set(original_sentences)

    ordered_sentences = []
    map_indices = {}
    done = set()
    for sent in original_sentences:
        if (sent in summary_sentences_set) and (sent not in done):
            map_indices[sent] = len(ordered_sentences)
            ordered_sentences.append(sent)
            done.add(sent)

    assert len(ordered_sentences) >= 1 and len(ordered_sentences) == len(done)
    occurrences = [0] * len(ordered_sentences)
    for sent in summary_sentences:
        if sent in original_sentences_set:
            occurrences[map_indices[sent]] += 1

    assert min(occurrences) >= 1, document + ' : ' + str(occurrences)

    return ordered_sentences, occurrences


def word_count(sentences):
    cnt = 0
    for sent in sentences:
        cnt += len(sent.split())
    return cnt

def generate_wMVC_summ(input_path,reference_path,output_path,limit):
    
    for doc in listdir(input_path):
        with open(input_path+doc,"r") as f:
            txt = f.read()
            if txt=='' or txt=='None.':
                open(output_path + doc, 'w', encoding='utf8').write('')
                continue
        sent_tokens, factors = get_sentences_with_factors(input_path,reference_path,doc)

#         if sent_tokens[0].lower() == 'none.':
#             open(output_path + doc, 'w', encoding='utf8').write('')
#             continue

        if word_count(sent_tokens) < 250:
            open(output_path + doc, 'w', encoding='utf8').write('\n\n'.join(sent_tokens))
            continue

        occurrence, filtered_sentences = compute_occurrences(sent_tokens)

        dist = ndarray([len(sent_tokens), len(sent_tokens)])

        for i in range(len(sent_tokens)):
            for j in range(len(sent_tokens)):
                if i == j:
                    dist[i][j] = 1
                    continue

                s1 = filtered_sentences[i]
                s2 = filtered_sentences[j]
                intersection = s1 & s2

                numerator = 0
                for word in intersection:
                    numerator += log(len(sent_tokens) / occurrence[word])

                denominator = 0
                for word in s2:
                    denominator += log(len(sent_tokens) / occurrence[word])

                if denominator >= numerator >= 0 and denominator > 0:
                    dist[i][j] = numerator / denominator
                else:
                    dist[i][j] = 0

        dist_nonzero = array(dist.flatten())
        dist_nonzero = list(filter(lambda x: x > 1e-6, dist_nonzero))
        dist_nonzero.sort()
        dist_nonzero = dist_nonzero[:len(dist_nonzero) - len(sent_tokens)]

        threshold = quantile(dist_nonzero, 0.5)
        large = 2 * max(factors) * len(sent_tokens)

        vertices = [(i, {'weight': large - factors[i] * (sum(dist[i]) - 1)})
                    for i in range(len(sent_tokens))]

        edges = []
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                cur_score = max(dist[i][j], dist[j][i])
                if cur_score >= threshold:
                    edges.append((i, j, {'length': cur_score}))

        G = Graph()
        G.add_nodes_from(vertices)
        G.add_edges_from(edges)

        wMVC = min_weighted_vertex_cover(G, 'weight')

        tops = sorted([vertices[i] for i in wMVC],
                      key=lambda x: x[1]['weight'])

        write_summary(tops, sent_tokens, limit, doc, output_path)
        
def main():
    root_path = "../Data/Input-wMVC/"
    for section in os.listdir(root_path):        
        input_path = root_path+section+'/'
        reference_path = input_path
        output_path = f"../Data/Input-BART/{section}/"
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        
        if section=='Conclusions':
            generate_wMVC_summ(input_path,reference_path,output_path,150)
        else:
            generate_wMVC_summ(input_path,reference_path,output_path,170)
            
if __name__=='__main__':
    main()
            