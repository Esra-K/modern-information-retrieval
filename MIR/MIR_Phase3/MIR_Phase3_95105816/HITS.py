import json
from collections import defaultdict

with open('spiders/result.json') as o:
    big_dict = json.load(o)


def hits(num_of_authors):
    global big_dict
    aux_dict = {article['id']: article for article in big_dict}
    outgoing_graph = defaultdict(list)
    auth_set = set()
    for article_id, article in aux_dict.items():
        writers = article['authors']
        reference_list = [r for r in article['references'] if r in aux_dict.keys()]
        for w in writers:
            for ref in reference_list:
                reference_authors = aux_dict[ref]['authors']
                for master in reference_authors:
                    outgoing_graph[w].append(master)

    threshold = 10 ** -4
    for k, v in outgoing_graph.items():
        auth_set.add(k)
        for v1 in v:
            auth_set.add(v1)
    h = dict.fromkeys(auth_set, 1/len(list(auth_set)))
    while True:
        hlast = h
        h = dict.fromkeys(auth_set, 0)
        a = dict.fromkeys(auth_set, 0)

        for author, referenced_authors in outgoing_graph.items():
            for master_author in referenced_authors:
                if master_author in outgoing_graph.keys():
                    a[master_author] += hlast[author]

        for author, referenced_authors in outgoing_graph.items():
            for master_author in referenced_authors:
                if master_author in hlast.keys():
                    h[author] += a[master_author]

        normalization_coefficient = 1.0 / max(h.values())
        for referring_author in h:
            h[referring_author] *= normalization_coefficient

        normalization_coefficient = 1.0 / max(a.values())
        for referred_author in a:
            a[referred_author] *= normalization_coefficient

        error = sum([abs(h[n] - hlast[n]) for n in h])
        if error < threshold:
            break

    normalization_coefficient = 1.0 / sum(h.values())
    for referring_author in h:
        h[referring_author] *= normalization_coefficient

    normalization_coefficient = 1.0 / sum(a.values())
    for referred_author in a:
        a[referred_author] *= normalization_coefficient
    return sorted(a, key=a.get, reverse=True)[:num_of_authors]


n = int(input("Enter n\n"))
print(hits(n))

