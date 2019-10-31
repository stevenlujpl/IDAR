#!/usr/bin/env python
# find_difference.py
# Find the differences between zooniverse csv and gold standard csv files. 
# Note: this is only working if gold standard csv is a subset of zooniverse csv.
# The output is in zooniverse csv format.
# 
# Steven Lu 5/7/2018

import csv
import os
import sys
import numpy as np

def main(zooniverse_csv, gold_standard_csv, merged_csv):
    if not os.path.isfile(zooniverse_csv):
        print 'Zooniverse csv file %s does not exist.' % zooniverse_csv
        sys.exit()

    if not os.path.isfile(gold_standard_csv):
        print 'Gold standard csv file %s does not exist.' % gold_standard_csv

    # read zooniverse csv file in python list
    f = open(zooniverse_csv, 'rb')
    reader = csv.reader(f, delimiter=',')
    zooniverse_list = list(reader)
    f.close()

    # read gold standard csv file in python list
    f = open(gold_standard_csv, 'rb')
    reader = csv.reader(f, delimiter=',')
    gold_standard_list = list(reader)
    f.close()

    # find differences
    for g_item in gold_standard_list:
        duplicates = [x for x in zooniverse_list if x[13] == g_item[0]]
        for d in duplicates:
            zooniverse_list.remove(d)

    # write output
    f = open(merged_csv, 'wb')
    writer = csv.writer(f)
    writer.writerows(zooniverse_list)
    f.close()
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('zooniverse_csv', metavar='zooniverse csv')
    parser.add_argument('gold_standard_csv', metavar='gold standard csv')
    parser.add_argument('merged_csv', metavar='merged csv')

    args = parser.parse_args()
    main(**vars(args))
