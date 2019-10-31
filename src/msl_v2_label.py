#!/usr/bin/env python
# msl_v2_label.py
# Steven Lu, 7/24/2019


import os
import sys
from parser.cd_list_parser import CDListParser
from collection.ambiguous_collection import AmbiguousCollection
from html_builder.msl_v2_html_builder import MslV2HTMLBuilder


def main(list_file, image_dir, template_dir, out_dir, user):
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

    cd_parser = CDListParser(list_file)
    raw_collection = cd_parser.parse()
    label_collection = AmbiguousCollection([])
    html_builder = MslV2HTMLBuilder(image_dir, template_dir, out_dir, user)

    for subject in raw_collection.get_subjects():
        label_collection.add_subject(subject)

    label_collection.build_html(html_builder)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument('list_file', help='A list of filenames to be labeled.')
    parser.add_argument('image_dir', help='The directory of all images')
    parser.add_argument('template_dir', help='The directory of HTML template '
                                             'files.')
    parser.add_argument('out_dir')
    parser.add_argument('-u', '--user', type=str, default='user',
                        help='A string that will be used as a part of the '
                             'keys of localStorage')

    args = parser.parse_args()
    main(**vars(args))
