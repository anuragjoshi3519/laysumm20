from math import log
from os import mkdir
from os.path import isdir

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from numpy import ndarray, array, quantile
from regex import I, sub


def word_count(sentence: str) -> int:
    return len(word_tokenize(sentence))


def document_word_count(sentences: list) -> int:
    return sum([word_count(sentence) for sentence in sentences])


def get_sentence_tokens(text: str) -> list:
    result = []
    for sent in [s.strip() for s in text.split('\n') if len(s.strip()) > 0]:
        for puts in sent_tokenize(sent):
            result.append(puts)
    return result


def compute_occurrences(sentences: list) -> tuple:
    filtered = []
    stop_words = stopwords.words('english')

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


def compute_entailment(sentence_tokens: list) -> ndarray:
    dist = ndarray([len(sentence_tokens), len(sentence_tokens)])
    occurrence, filtered_sentences = compute_occurrences(sentence_tokens)

    for i in range(len(sentence_tokens)):
        for j in range(len(sentence_tokens)):
            if i == j:
                dist[i][j] = 1
                continue

            s1 = filtered_sentences[i]
            s2 = filtered_sentences[j]
            intersection = s1 & s2

            numerator = 0
            for word in intersection:
                numerator += log(len(sentence_tokens) / occurrence[word])

            denominator = 0
            for word in s2:
                denominator += log(len(sentence_tokens) / occurrence[word])

            if denominator >= numerator >= 0 and denominator > 0:
                dist[i][j] = numerator / denominator
            else:
                dist[i][j] = 0

    return dist


def compute_threshold(dist: ndarray, partition: float) -> float:
    dist_nonzero = array(dist.flatten())
    dist_nonzero = list(filter(lambda x: x > 1e-6, dist_nonzero))
    if len(dist_nonzero) <= len(dist):
        return 0.0
    dist_nonzero.sort()
    dist_nonzero = dist_nonzero[:len(dist_nonzero) - len(dist)]
    return quantile(dist_nonzero, partition)


def get_input_with_reference(input_path: str, reference_path: str, filename: str) -> tuple:
    cur_doc = open(input_path + filename, 'r', encoding='utf8').read()
    ref_doc = open(reference_path + filename, 'r', encoding='utf8').read()

    cur_doc = sub(r' +', ' ', cur_doc, flags=I)
    ref_doc = sub(r' +', ' ', ref_doc, flags=I)

    return cur_doc, ref_doc


def get_sentences_with_factors(input_path: str, reference_path: str, filename: str) -> tuple:
    cur_doc, ref_doc = get_input_with_reference(input_path, reference_path, filename)

    summary_sentences = get_sentence_tokens(cur_doc)
    summary_sentences_set = set(summary_sentences)

    original_sentences = get_sentence_tokens(ref_doc)
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
    occurrences = [0 for _ in range(len(ordered_sentences))]
    for sent in summary_sentences:
        if sent in original_sentences_set:
            occurrences[map_indices[sent]] += 1

    assert min(occurrences) >= 1, filename + ' : ' + str(occurrences)

    return ordered_sentences, occurrences


def write_summary(write_to_path: str, filename: str, word_limit: int, sentence_tokens: list,
                  ordered_sentence_indices: list):
    if not isdir(write_to_path):
        mkdir(write_to_path)

    summary_indices1 = []
    count1 = 0
    for index in ordered_sentence_indices:
        cur_len = len(sentence_tokens[index].split())
        if count1 + cur_len > word_limit:
            break
        count1 += cur_len
        summary_indices1.append(index)

    summary1 = []
    for index in sorted(summary_indices1):
        summary1.append(sentence_tokens[index])

    summary_indices2 = []
    count2 = 0
    for index in ordered_sentence_indices:
        if count2 >= word_limit:
            break
        count2 += len(sentence_tokens[index].split())
        summary_indices2.append(index)

    summary2 = []
    for index in sorted(summary_indices2):
        summary2.append(sentence_tokens[index])

    summary = ''
    if abs(word_limit - count1) < abs(word_limit - count2):
        summary += '\n\n'.join(summary1)
    else:
        summary += '\n\n'.join(summary2)

    open(write_to_path + filename, 'w', encoding='utf8').write(summary)


def create_edge_set(dist: ndarray, threshold: float) -> list:
    edges = []
    for i in range(len(dist)):
        for j in range(i + 1, len(dist[i])):
            if dist[i][j] > dist[j][i] and dist[i][j] >= threshold:
                edges.append((i, j, {'length': dist[i][j]}))
            elif dist[j][i] > dist[i][j] and dist[j][i] >= threshold:
                edges.append((j, i, {'length': dist[j][i]}))
    return edges
