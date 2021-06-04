import json
from collections import defaultdict
from math import fabs
import json

# Dictionary fields:
# id
# title
# abstract
# references
# date
# authors

with open("spiders/result.json") as o:
    dict_list = json.load(o)


def page_rank():
    global dict_list

    id_set = set([e['id'] for e in dict_list])
    # print(len(id_set))
    old_score_list = defaultdict(float)
    l = 1 / len(id_set)
    for i_d in id_set:
        old_score_list[i_d] = l
    new_score_list = defaultdict(float)
    outer_links = defaultdict(float)
    referers = defaultdict(list)
    for i, e in enumerate(dict_list):
        id1 = e['id']
        # print(id1, e['references'])
        for r, rid in enumerate(e['references']):
            if rid in id_set:
                outer_links[id1] += 1
                referers[rid] += [id1]
        # print('here', len(list(referers.keys())))
    threshold = 10 ** -3
    while True:
        total = 0
        for rid, rid_list in referers.items():
            for referer in rid_list:
                addition = old_score_list[referer] / outer_links[referer]
                new_score_list[rid] += old_score_list[referer] / outer_links[referer]
                total += addition

        for k, v in new_score_list.items():
            v /= total

        epsilon = 0
        for i_d in old_score_list.keys():
            epsilon += fabs(old_score_list[i_d] - new_score_list[i_d])

        if epsilon > threshold:
            break

        old_score_list = new_score_list
        new_score_list = dict.fromkeys(new_score_list, 0)

    return new_score_list


scores = page_rank()

for d in dict_list:
    d.update({"page_rank": scores[d["id"]]})

# print(len(dict_list))

with open('ranked_results.json', 'w') as f:
    json.dump(dict_list, f)
