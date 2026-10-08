#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
import matplotlib.pyplot as plt
from collections import Counter,defaultdict

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# sort by value from high to low and keep top 10
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)[:10]

# sort the top 10 from low to high
items = sorted(items, key=lambda item: item[1])

# separate keys and values
keys = [item[0] for item in items]
values = [item[1] for item in items]

# create bar graph
plt.bar(keys, values)

plt.xlabel('Key')

if args.percent:
    plt.ylabel('Percent')
else:
    plt.ylabel('Count')

plt.title(args.key)

plt.xticks(rotation=45)
plt.tight_layout()

# save as png
output_path = args.input_path + '.' + args.key.replace('#', '') + '.png'
plt.savefig(output_path)

print('saving', output_path)


