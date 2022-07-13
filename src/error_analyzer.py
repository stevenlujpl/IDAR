#!/usr/bin/env python
# error_analyzer.py
# This script takes a label file and a prediction file as inputs. Both files 
# should be in caffe format (image_id class_as_integer). The output is a static
# HTML web page that contains images, whose predictions are different from their
# labels, to be further analyzed. 
#
# Steven Lu 1/9/2019

import os
import sys
import random

from parser.ea_csv_parser import EACSVParser
from collection.ambiguous_collection import AmbiguousCollection
from html_builder.error_html_builder import ErrorHTMLBuilder

def main(image_dir, label_file, preds_file, template_dir, out_dir,
         classmap_file=None, num=-1):
    # Check arguments up front
    if not os.path.isdir(image_dir):
        print('[ERROR] Could not find image directory %s' % image_dir)
        sys.exit(1)

    if not os.path.exists(label_file):
        print('[ERROR] Could not find label file %s' % label_file)
        sys.exit(1)

    if not os.path.exists(preds_file):
        print('[ERROR] Could not find prediction file %s' % preds_file)

    # If output directory doesn't exist, create it.
    if not os.path.isdir(out_dir):
        print('Creating output directory %s' % out_dir)
        os.mkdir(out_dir)

    # If classmap file is provided, then make sure it exists.
    if classmap_file is not None and not os.path.isfile(classmap_file):
        print('[ERROR] Could not find classmap file %s' % classmap_file)
        sys.exit(1)

    ea_parser = EACSVParser(label_file, preds_file, classmap_file)
    raw_collection = ea_parser.parse()
    ea_collection = AmbiguousCollection([])
    html_builder = ErrorHTMLBuilder(image_dir, template_dir, out_dir)

    for subject in raw_collection.get_subjects():
        if subject.get_label() != subject.get_pred():
            ea_collection.add_subject(subject)

    # Randomly select the 'num' of mis-classified items to review.
    total_num = len(ea_collection.get_subjects())
    if 0 < num < total_num:
        subjects = ea_collection.get_subjects()
        random.shuffle(subjects)
        ea_collection.set_subjects(subjects[:num])
    else:
        print('[WARNING] The --num specified in the command line is either ' \
              'smaller than or equal to 0, or greater than the number of ' \
              'items in the collection. All the items will be used for error ' \
              'analysis.')

    # Build a static HTML page to further analyze mis-labeled images
    ea_collection.build_html(html_builder)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='%prog', 
        description='Create a static HTML page for analyzing mis-classified '
                    'images.',
        argument_default=argparse.SUPPRESS)
      
    parser.add_argument('image_dir', help='The directory of all images')
    parser.add_argument('label_file', help='Label file in caffe format')
    parser.add_argument('preds_file', help='Prediction file in caffe format')
    parser.add_argument('template_dir', help='The directory of HTML template '
                                             'files and libraries')
    parser.add_argument('out_dir', help='The output directory for the static '
                                        'HTML page')
    parser.add_argument('classmap_file', nargs='?',
                        help='This is an optional parameter for mapping the '
                             'class representations provided in label_file and '
                             'preds_file into something more meaningful.')
    parser.add_argument('-n', '--num', required=False, type=int,
                        help='The (non-negative) number of misclassified items to review (randomly selected)')

    args = parser.parse_args()
    main(**vars(args))
