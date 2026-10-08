#!/usr/bin/env python3

# command line args
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True)
parser.add_argument('--input_folder', default='outputs')
parser.add_argument('--output_path', default='hashtag_over_time.png')
args = parser.parse_args()

# imports
import os
import glob
import json
import datetime
import matplotlib.pyplot as plt

# dictionary to hold data for each hashtag
hashtag_counts = {}

for hashtag in args.hashtags:
    hashtag_counts[hashtag] = []

# store day-of-year values
days = []

# get all language output files
paths = sorted(glob.glob(os.path.join(args.input_folder, '*.lang')))

# scan through all mapped output files
for path in paths:

    # example filename:
    # geoTwitter20-03-12.zip.lang
    filename = os.path.basename(path)

    # extract date
    date_string = filename.replace('geoTwitter', '').replace('.zip.lang', '')

    date = datetime.datetime.strptime(date_string, '%y-%m-%d')

    # convert date to day of year
    day_of_year = date.timetuple().tm_yday
    days.append(day_of_year)

    # load daily counts
    with open(path) as f:
        counts = json.load(f)

    # get count for each requested hashtag
    for hashtag in args.hashtags:

        if hashtag in counts:
            daily_count = sum(counts[hashtag].values())
        else:
            daily_count = 0

        hashtag_counts[hashtag].append(daily_count)

# plot one line per hashtag
for hashtag in args.hashtags:
    plt.plot(days, hashtag_counts[hashtag], label=hashtag)

plt.xlabel('Day of Year')
plt.ylabel('Number of Tweets')
plt.title('Hashtag Usage During 2020')
plt.legend()
plt.tight_layout()

# save graph
plt.savefig(args.output_path)

print('saving', args.output_path)
