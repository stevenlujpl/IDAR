#!/usr/bin/env python
# outlier_image_analyzer.py
# Take in a set of images and feature vectors,
# and rank the images by outlierness (using an SVD),
# then create an HTML page for review.
#
# Kiri Wagstaff, 7/30/2018

import os, sys
import numpy as np
from numpy import linalg

from parser.landmarks_csv_parser import LandmarksCSVParser
from collection.ambiguous_collection import AmbiguousCollection
from html_builder.outlier_html_builder import OutlierHTMLBuilder
from entity.subject import Subject


def main(image_dir, feature_file, template_dir, out_dir, k, n):

    # Check arguments up front
    if not os.path.isdir(image_dir):
        print('Could not find image directory %s' % image_dir)
        sys.exit(1)

    if not os.path.exists(feature_file):
        print('Could not find feature file (.csv) %s' % feature_file)
        sys.exit(1)

    if not os.path.isdir(template_dir):
        print('Could not find template directory %s' % template_dir)
        sys.exit(1)

    # If output directory doesn't exist, create it
    if not os.path.isdir(out_dir):
        print('Creating output directory %s' % out_dir)
        os.mkdir(out_dir)

    # Read in the features (CSV)
    imagenames = []
    features   = []
    with open(feature_file, 'r') as csvfile:
        lines = csvfile.readlines()
        for line in lines:
            vals = line.strip().split(',')
            imagenames += [vals[0]]
            features   += [[float(x) for x in vals[1:]]]
    features = np.array(features).T

    # Sort images by decreasing SVD reconstruction error
    U, S, V = linalg.svd(features)
    print('SVD complete.')
    # Truncate SVD to k components
    U = U[:,0:k]
    # Project all data onto U
    mu     = np.mean(features, axis=1).reshape(-1,1) 
    proj   = np.dot(U.T, (features - mu))
    # Reconstruct
    reproj = np.dot(U, proj) + mu
    # Compute reconstruction error
    err    = features - reproj
    score  = np.sum(np.array(np.power(err, 2)), axis=0)
    # Sort in descending order
    sorted = score.argsort()[::-1]
    sorted_imagenames = [imagenames[i] for i in sorted]

    # All of the images go here
    outlier_collection = AmbiguousCollection([])
    # Keep only the first n
    for i, im in zip(sorted, sorted_imagenames)[0:n]:
        # Use fake indices and labels
        s = Subject(i, im)
        s.add_record('', 'none', '')
        outlier_collection.add_subject(s)

    print('Showing top %d images' % n)

    # Create the HTML review page
    html_builder = OutlierHTMLBuilder(image_dir, template_dir, out_dir)

    # build a static HTML web to further analyze outlier records
    # (montage is included)
    outlier_collection.build_html(html_builder)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog=sys.argv[0],
        description='Create a static HTML page for analyzing outlier images',
        argument_default=argparse.SUPPRESS)

    parser.add_argument('image_dir',
                        help='The directory of all images')
    parser.add_argument('feature_file',
                        help='The csv file containing image feature vectors')
    parser.add_argument('template_dir', default='template',
                        help='The directory of HTML template files.')
    parser.add_argument('out_dir', 
                        help='The output directory for the static HTML page. '
                             'If the directory does not exist, '
                             'it will be created.')
    parser.add_argument('-k', default=100, type=int,
                        help='Number of SVD components to use in reconstruction (default=100).')
    parser.add_argument('-n', default=49, type=int,
                        help='Number of top outliers to show (default=49)')

    args = parser.parse_args()
    main(**vars(args))

