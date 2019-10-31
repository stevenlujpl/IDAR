#!/usr/bin/env python
# ambiguous_label_analyzer.py
# The script provides the following functionalities:
# 1. extract ambiguous subjects and construct them into a static html page.
# 2. extract gold standard subjects, and write them out as a CSV file.
#
# Steven Lu 4/20/2018

import os, sys

from parser.landmarks_csv_parser import LandmarksCSVParser
from collection.gold_standard_collection import GoldStandardCollection
from collection.ambiguous_collection import AmbiguousCollection
from rule.landmarks_rule import LandmarksRule
from html_builder.landmarks_html_builder import LandmarksHTMLBuilder

def main(image_dir, csv_file, template_dir, out_dir):

    # Check arguments up front
    if not os.path.isdir(image_dir):
        print('Could not find image directory %s' % image_dir)
        sys.exit(1)

    if not os.path.exists(csv_file):
        print('Could not find label file (.csv) %s' % csv_file)
        sys.exit(1)

    if not os.path.isdir(template_dir):
        print('Could not find template directory %s' % template_dir)
        sys.exit(1)

    # If output directory doesn't exist, create it
    if not os.path.isdir(out_dir):
        print('Creating output directory %s' % out_dir)
        os.mkdir(out_dir)

    csvparser = LandmarksCSVParser(csv_file, out_dir)
    raw_collection = csvparser.parse()

    landmarks_rule = LandmarksRule(retirement_count=3)
    gold_standard_collection = GoldStandardCollection([])
    ambiguous_collection = AmbiguousCollection([])
    html_builder = LandmarksHTMLBuilder(image_dir, template_dir, out_dir)

    skip_counter = 0
    for subject in raw_collection.get_subjects():
        if landmarks_rule.is_gold_standard(subject):
            annotation = landmarks_rule.extract_gold_standard_annotation(subject)
            gold_standard_collection.add_subject(subject, annotation)
        elif landmarks_rule.is_ambiguous(subject):
            ambiguous_collection.add_subject(subject)
        else:
            # subjects haven't been retired
            skip_counter += 1

    print 'Gold standard records counts: %d' % \
          len(gold_standard_collection.get_subjects())
    print 'Ambiguous records counts: %d' % \
          len(ambiguous_collection.get_subjects())
    print 'Skipped records counts: %d\n' % skip_counter

    # save gold standard records
    gold_standard_collection.save_csv(csvparser)

    # build a static HTML web to further analyze ambiguous records
    ambiguous_collection.build_html(html_builder)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='%prog',
        description='Create a static HTML page for analyzing ambiguous labels',
        argument_default=argparse.SUPPRESS)

    parser.add_argument('image_dir', 
                        help='The directory of all images')
    parser.add_argument('csv_file', 
                        help='The csv file that contains all annotations')
    parser.add_argument('template_dir', default='template',
                        help='The directory of HTML template files.')
    parser.add_argument('out_dir', 
                        help='The output directory for the static HTML page and'
                             ' the gold standard csv file. If the directory '
                             'does not exist, it will be created.')

    args = parser.parse_args()
    main(**vars(args))

