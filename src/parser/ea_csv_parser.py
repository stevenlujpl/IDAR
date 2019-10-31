# ea_csv_parser.py
# "ea" stands for error analysis. This script parses "label" and "pred" csv
# files into collection object. 
#
# Steven Lu 1/9/2019

import sys

from collection.ea_raw_collection import EARawCollection


class EACSVParser:
    # #########################################################
    # Example label file format:
    # ESP_016568_1710_RED-0088.jpg 0
    # ESP_016568_1710_RED-0088-r90.jpg 0
    # ESP_016568_1710_RED-0088-r180.jpg 0
    # ...
    # ESP_016568_1710_RED-0088-fh.jpg 0
    # ESP_016568_1710_RED-0088-fv.jpg 0
    # ESP_016568_1710_RED-0088-brt.jpg 0
    #
    # Example prediction file format:
    # ESP_016568_1710_RED-0088.jpg    0       1.00
    # ESP_016568_1710_RED-0088-r90.jpg        0       0.94
    # ESP_016568_1710_RED-0088-r180.jpg       0       1.00
    # ...
    # ESP_016568_1710_RED-0088-fh.jpg 0       0.99
    # ESP_016568_1710_RED-0088-fv.jpg 0       0.98
    # ESP_016568_1710_RED-0088-brt.jpg        0       1.00
    #
    # Example classmap file format:
    # 0,other
    # 1,crater
    # 2,dark dune
    # 3,slope streak
    # 4,bright dune
    # 5,impact ejecta
    # 6,swiss cheese
    # 7,spider
    # #########################################################
    def __init__(self, label_path, pred_path, classmap_path):
        self._label_path = label_path
        self._pred_path = pred_path
        self._classmap_path = classmap_path

    def get_label_path(self):
        return self._label_path

    def set_label_path(self, label_path):
        self._label_path = label_path

    def get_pred_path(self):
        return self._pred_path

    def set_pred_path(self, pred_path):
        self._pred_path = pred_path

    def get_classmap_path(self):
        return self._classmap_path

    def set_classmap_path(self, classmap_path):
        self._classmap_path = classmap_path

    # parse() throws IOError if the path to csv file is incorrect.
    def parse(self):
        # Open and read label and prediction files
        label_file = open(self._label_path, 'r')
        label_lines = label_file.readlines()
        pred_file = open(self._pred_path, 'r')
        pred_lines = pred_file.readlines()

        # Create a dict for classmap if the file is provided.
        if self._classmap_path is not None:
            classmap_file = open(self._classmap_path, 'r')
            classmap_lines = classmap_file.readlines()

            class_dict = dict()
            for l in classmap_lines:
                t = l.strip().split(',')
                class_dict[t[0]] = t[1]

        # Assume image names in pred_lines are a subset of label_lines.
        # Prune label_lines to match.
        nlabels = len(label_lines)
        pred_filenames = [p.split()[0] for p in pred_lines]
        label_lines = [l for l in label_lines 
                       if l.split()[0] in pred_filenames]
        nlabels_pruned = len(label_lines)
        if nlabels_pruned != nlabels:
            print('Pruned %d labels to %d to match predictions.' % 
                  (nlabels, nlabels_pruned))

        raw_collection = EARawCollection([])
        for l, p in zip(label_lines, pred_lines):
            l_tokens = l.split()
            p_tokens = p.split()

            # The orders of the items in the label and prediction files are 
            # expected to be the same.
            if l_tokens[0] != p_tokens[0]:
                print '[ERROR] The orders of the items in the label and ' \
                      'prediction files are different.'
                sys.exit(1)

            id = l_tokens[0]
            conf = p_tokens[2]

            if self._classmap_path is not None and len(class_dict.keys()) > 0:
                label = class_dict[l_tokens[1]]
                pred = class_dict[p_tokens[1]]
            else:
                label = l_tokens[1]
                pred = p_tokens[1]

            raw_collection.add_subject(id, label, pred, conf)

        # close files
        label_file.close()
        pred_file.close()

        if self._classmap_path is not None:
            classmap_file.close()

        return raw_collection
