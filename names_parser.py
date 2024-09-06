from collections import defaultdict
import os
import json
import metaphone
import jellyfish

def rec_default():
    return defaultdict(rec_default)


# name_struct = rec_default()
boy_name_struct = defaultdict(int)
girl_name_struct = defaultdict(int)

directory = os.fsencode('./names')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith('.txt'):
        with open('./names/' + filename) as fd:
            for entry in fd:
                (name, gender, total) = entry.split(',')
                if gender == 'M':
                    boy_name_struct[name] += int(total)
                elif gender == 'F':
                    girl_name_struct[name] += int(total)
                # previous_total = name_struct[name][gender].setdefault('count', 0)
                # name_struct[name][gender]['count'] = previous_total + int(total)

pron_alias = {}
as_said = defaultdict(list)
for name in sorted(boy_name_struct.keys(), key=lambda name: boy_name_struct[name]):
    # (pron, pron2) = metaphone.doublemetaphone(name)

    # dest = pron
    # if pron in pron_alias or pron2 in pron_alias:
    #     dest = pron_alias.get(pron, pron_alias.get(pron2))

    # pron_alias[pron] = dest
    # if pron2:
    #     pron_alias[pron2] = dest

    # as_said[dest].append(name)

    pron = jellyfish.match_rating_codex(name)
    as_said[pron].append(name)

# print('' in pron_alias)

# for names in sorted(as_said.values(), key=lambda names: boy_name_struct[max(names, key=lambda name: boy_name_struct[name])], reverse=True):
for pron, names in sorted(as_said.items(), key=lambda prams: boy_name_struct[max(prams[1], key=lambda name: boy_name_struct[name])], reverse=True):
    print('{} = {}: {} variants, {} observations: {}'.format(pron, max(names, key=lambda name: boy_name_struct[name]), len(names), sum([boy_name_struct[name] for name in names]), names))
