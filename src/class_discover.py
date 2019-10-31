#!/usr/bin/env python
# class_discover.py
# This script takes a DEMUD ordered list file, and generates a static HTML page
# for class discovery.
#
# Steven Lu 5/20/2019

import os
import sys
from parser.cd_list_parser import CDListParser
from collection.ambiguous_collection import AmbiguousCollection
from html_builder.cd_html_builder import CDHtmlBuilder


def main(image_dir, list_file, template_dir, out_dir):
    if not os.path.exists(image_dir):
        print '[ERROR] Could not find image directory %s' % image_dir
        sys.exit(1)

    if not os.path.exists(list_file):
        print '[ERROR] Could not find list file %s' % list_file
        sys.exit(1)

    # If output directory doesn't exist, create it.
    if not os.path.isdir(out_dir):
        print 'Creating output directory %s' % out_dir
        os.mkdir(out_dir)

    cd_parser = CDListParser(list_file)
    raw_collection = cd_parser.parse()
    cd_collection = AmbiguousCollection([])
    html_builder = CDHtmlBuilder(image_dir, template_dir, out_dir)

    for subject in raw_collection.get_subjects():
        cd_collection.add_subject(subject)

    cd_collection.build_html(html_builder)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='%prog',
                                     description='Class discovery script',
                                     argument_default=argparse.SUPPRESS)

    parser.add_argument('image_dir', help='The directory of all images')
    parser.add_argument('list_file', help='Label file in caffe format')
    parser.add_argument('template_dir', help='The directory of HTML template '
                                             'files and libraries')
    parser.add_argument('out_dir', help='The output directory for the static '
                                        'HTML page')

    args = parser.parse_args()
    main(**vars(args))
