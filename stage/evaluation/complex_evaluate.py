import xml.etree.ElementTree as ET
from stage.evaluation.tree_similarity import tree_sim, tree_size, post_order
import re
import io

def xml_to_tree(t):
    att_keys = sorted(list(t.attrib.keys()))
    att_pairs = ', '.join([f'{k}: {t.attrib[k]}' for k in att_keys])
    tag = f'{t.tag} {att_pairs}'

    children = sorted([xml_to_tree(c) for c in t], key=lambda x: x[0])
    return tag, children

def load_maps(path, ignore_errors = False):
    tree = ET.parse(path)
    root = tree.getroot()

    maps = []

    for c in root:
        for c1 in c:
            if not c1.tag.endswith('map'):
                continue
            if ignore_errors:
                try:
                    cell = c1.find('{http://knowledgeweb.semanticweb.org/heterogeneity/alignment#}Cell')
                    ent1 = cell.find('{http://knowledgeweb.semanticweb.org/heterogeneity/alignment#}entity1')
                    ent2 = cell.find('{http://knowledgeweb.semanticweb.org/heterogeneity/alignment#}entity2')

                    t1 = ent1[0] if len(ent1) > 0 else ent1
                    t2 = ent2[0] if len(ent2) > 0 else ent2

                    maps.append((xml_to_tree(t1), xml_to_tree(t2)))
                except:
                    pass
            else:
                cell = c1.find('{http://knowledgeweb.semanticweb.org/heterogeneity/alignment#}Cell')
                ent1 = cell.find('{http://knowledgeweb.semanticweb.org/heterogeneity/alignment#}entity1')
                ent2 = cell.find('{http://knowledgeweb.semanticweb.org/heterogeneity/alignment#}entity2')

                t1 = ent1[0] if len(ent1) > 0 else ent1
                t2 = ent2[0] if len(ent2) > 0 else ent2

                maps.append((xml_to_tree(t1), xml_to_tree(t2)))

    return maps

def maximize_assign(m):

    preferences = {}

    for i, p in enumerate(m):
        preferences[i] = list(sorted(enumerate(p), key=lambda x: x[1], reverse=True))

    unassigned_pairs = list(range(len(m)))

    assigned_pairs = {}

    while unassigned_pairs:
        pair = unassigned_pairs.pop()
        pair_similarities = preferences[pair]
        if len(pair_similarities) == 0:
            continue

        next_similarity = pair_similarities.pop(0)

        if next_similarity[0] in assigned_pairs:
            if next_similarity[1] > assigned_pairs[next_similarity[0]][1]:
                unassigned_pairs.append(assigned_pairs[next_similarity[0]][0])
                assigned_pairs[next_similarity[0]] = (pair, next_similarity[1])
            else:
                unassigned_pairs.append(pair)
        else:
            assigned_pairs[next_similarity[0]] = (pair, next_similarity[1])

    return assigned_pairs


def evaluate_edoal_string(p1, p2, w = 0.5, sim_func = tree_sim, ignore_errors = False):
    return evaluate_edoal(io.StringIO(initial_value=p1), io.StringIO(initial_value=p2), w, sim_func, ignore_errors=ignore_errors)

def evaluate_edoal(p1, p2, w = 0.5, sim_func = tree_sim, ignore_errors = False):
    maps1 = load_maps(p1, ignore_errors=ignore_errors)
    maps2 = load_maps(p2, ignore_errors=ignore_errors)

    p_simple_count = 0
    p_complex_count = 0
    for m1, m2 in maps1:
        if tree_size(m1) == 1 and tree_size(m2) == 1:
            p_simple_count += 1
        else:
            p_complex_count += 1

    r_simple_count = 0
    r_complex_count = 0
    for m1, m2 in maps2:
        if tree_size(m1) == 1 and tree_size(m2) == 1:
            r_simple_count += 1
        else:
            r_complex_count += 1

    sl = []

    for mt1, mt2 in maps1:
        ms = []
        for m1, m2 in maps2:
            ms.append((sim_func(mt1, m1) + sim_func(mt2, m2)) / 2)

        sl.append(ms)

    assigns = maximize_assign(sl)

    p_simple_assigns = {}
    p_complex_assigns = {}
    r_simple_assigns = {}
    r_complex_assigns = {}

    for k, v in assigns.items():
        mt1, mt2 = maps1[v[0]]
        m1, m2 = maps2[k]
        if tree_size(m1) == 1 and tree_size(m2) == 1:
            r_simple_assigns[k] = v
        else:
            r_complex_assigns[k] = v

        if tree_size(mt1) == 1 and tree_size(mt2) == 1:
            p_simple_assigns[k] = v
        else:
            p_complex_assigns[k] = v

    sum1 = sum([v[1] for k, v in r_simple_assigns.items()])
    sum2 = sum([v[1] for k, v in r_complex_assigns.items()])
    sum3 = sum([v[1] for k, v in p_simple_assigns.items()])
    sum4 = sum([v[1] for k, v in p_complex_assigns.items()])

    rdiv = (1 - w) * r_simple_count + w * r_complex_count
    pdiv = (1 - w) * p_simple_count + w * p_complex_count
    soft_recall = ((1 - w) * sum1 + w * sum2) / rdiv if rdiv > 0 else 0
    soft_precision = ((1 - w) * sum3 + w * sum4) / pdiv if pdiv > 0 else 0
    soft_fmeasure = 2 * soft_recall * soft_precision / (
                soft_recall + soft_precision) if soft_recall + soft_precision > 0 else 0
    return soft_precision, soft_recall, soft_fmeasure


def filter_entities(n):
    return [x.split(' ')[1] for x in re.findall(r'resource: http://[^\s]+', n)] + [x.split(' ')[1] for x in re.findall(r'about: http://[^\s]+', n)]


def jaccard(s1, s2):
    return len(s1.intersection(s2)) / len(s1.union(s2)) if len(s1.union(s2)) > 0 else 0

def jaccard_sim(e1, e2):
    s1 = set()
    s2 = set()
    post_order(e1, lambda x, y: s1.update(filter_entities(y[0])))
    post_order(e2, lambda x, y: s2.update(filter_entities(y[0])))

    return jaccard(s1, s2)