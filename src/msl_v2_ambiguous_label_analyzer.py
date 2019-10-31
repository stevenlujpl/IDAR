#!/usr/bin/env python
# msl_v2_ambiguous_label_analyzer.py
# Steven Lu, 8/21/2019


import os
import sys
from parser.msl_v2_consolidated_list_parser import MSLV2ConsolidatedListParser
from collection.gold_standard_collection import GoldStandardCollection
from collection.ambiguous_collection import AmbiguousCollection
from rule.msl_v2_rule import MSLV2Rule
from html_builder.msl_v2_ambiguous_html_builder import MSLV2AmbiguousHTMLBuilder


def main(list_file, image_dir, template_dir, out_dir):
    # Check arguments up front
    if not os.path.isdir(image_dir):
        print('Could not find image directory %s' % image_dir)
        sys.exit(1)

    if not os.path.exists(list_file):
        print('Could not find label file (.csv) %s' % list_file)
        sys.exit(1)

    if not os.path.isdir(template_dir):
        print('Could not find template directory %s' % template_dir)
        sys.exit(1)

    # If output directory doesn't exist, create it
    if not os.path.isdir(out_dir):
        print('Creating output directory %s' % out_dir)
        os.mkdir(out_dir)

    msl_v2_parser = MSLV2ConsolidatedListParser(list_file, out_dir)
    raw_collection = msl_v2_parser.parse()

    msl_v2_rule = MSLV2Rule(retirement_count=3)
    gold_standard_collection = GoldStandardCollection([])
    ambiguous_collection = AmbiguousCollection([])
    html_builder = MSLV2AmbiguousHTMLBuilder(image_dir, template_dir, out_dir)

    skip_counter = 0
    for subject in raw_collection.get_subjects():
        if msl_v2_rule.is_gold_standard(subject):
            annotation = msl_v2_rule.extract_gold_standard_annotation(subject)
            gold_standard_collection.add_subject(subject, annotation)
        elif msl_v2_rule.is_ambiguous(subject):
            ambiguous_collection.add_subject(subject)
        else:
            skip_counter += 1

    print 'Gold standard records counts: %d' % \
          len(gold_standard_collection.get_subjects())
    print 'Ambiguous records counts: %d' % \
          len(ambiguous_collection.get_subjects())
    print 'Skipped records counts: %d\n' % skip_counter

    # Save gold standard records
    gold_standard_collection.save_csv(msl_v2_parser)

    # build a static HTML web to further analyze ambiguous subjects
    ambiguous_collection.build_html(html_builder)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument('list_file', help='Consolidated label file.')
    parser.add_argument('image_dir', help='The directory of all images')
    parser.add_argument('template_dir', help='The directory of HTML template '
                                             'files.')
    parser.add_argument('out_dir')

    args = parser.parse_args()
    main(**vars(args))
