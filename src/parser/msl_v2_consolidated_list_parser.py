# msl_v2_consolidated_list_parser.py
# This script parses the msl v2 consolidated list, and extracts image
# IDs (2nd column), annotations (3rd column), and annotators (4th column).
# Example consolidated list format:
# tool id,1591ML0081110040605082E01_DRCL.jpg,Wheel,kiri
# tool id,1793MH0007110030700805C00_DRCL.jpg,Sand,kiri
# tool id,1679MH0006490020603548I01_DRCL.jpg,Outcrop,kiri
# tool id,1702MH0007140030604290I01_DRCL.jpg,Outcrop,kiri
# tool id,1727ML0090210030701546I01_DRCL.jpg,Artifact,kiri
#
# Steven Lu 8/21/2019

import csv
import os
import errno
from collection.raw_collection import RawCollection


class MSLV2ConsolidatedListParser:
    def __init__(self, list_path, out_dir):
        self._list_path = list_path
        self._out_dir = out_dir

    def get_list_path(self):
        return self._list_path

    def set_list_path(self, list_path):
        self._list_path = list_path

    def parse(self):
        list_file = open(self._list_path, 'r')
        list_lines = list_file.readlines()

        print 'Processing MSL v2 consolidated list file: %s' % \
              os.path.abspath(self._list_path)

        raw_collection = RawCollection([])

        for line in list_lines:
            classification_id, subject_id, annotation, annotator = \
                line.strip().split(',')

            # Note: the second parameter of raw_collection.add_subject() method
            # is filename. In this case, subject_id is filename, so we just use
            # the subject_id as filename.
            raw_collection.add_subject(subject_id, subject_id,
                                       classification_id, annotation, annotator)

        list_file.close()

        return raw_collection

    def save(self, subjects):
        print 'Writing gold standard subjects to %s/%s file.' % \
              (os.path.abspath(self._out_dir), 'gold_standard.csv')

        # if output directory doesn't exist, create it.
        if not os.path.isdir(self._out_dir):
            print 'Create output directory %s' % os.path.abspath(self._out_dir)
            try:
                os.makedirs(self._out_dir)
            except OSError:
                if OSError.errno == errno.EEXIST and \
                        os.path.isdir(self._out_dir):
                    pass
                else:
                    raise

        csvfile = open('%s/%s' % (self._out_dir, 'gold_standard.csv'), 'wb')
        csvwriter = csv.writer(csvfile, delimiter=',')

        for subject in subjects:
            subject_id = subject.get_subject_id()
            records = subject.get_records()
            if not len(records) == 1:
                print 'Subject with subject_id=%s contains more than 1 record,' \
                      ' which is unexpected. Skipped.'
                continue
            annotation = records[0].get_annotation()

            csvwriter.writerow([subject_id, annotation])

        csvfile.close()
