# landmarks_csv_parser.py
# Parse the landmarks csv file into a collection object. It also provides the
# functionality to save a collection object into a csv file.
#
# Steven Lu 4/23/2018

from collection.raw_collection import RawCollection
import csv_mapping as m

import csv
import json
import sys
import os
import errno

class LandmarksCSVParser:
    def __init__(self, csv_path, out_dir):
        self._csv_path = csv_path
        self._out_dir = out_dir

    def get_csv_path(self):
        return self._csv_path

    def set_csv_path(self, csv_path):
        self._csv_path = csv_path

    def get_out_dir(self):
        return self._out_dir

    def set_out_dir(self, out_dir):
        self._out_dir = out_dir

    # parse() throws IOError if the path to csv file is incorrect.
    def parse(self):
        csvfile = open(self._csv_path, 'rb')
        csvreader = csv.reader(csvfile, delimiter=',')

        if m.landmarks_is_title_first_row:
            # skip the first header row
            csvreader.next()

        raw_collection = RawCollection([])
        processed_counter = 0
        skipped_counter = 0

        print 'Processing csv file %s' % os.path.abspath(self._csv_path)
        for row in csvreader:
            classification_id = row[m.landmarks_mapping['classification_id']]
            annotator = row[m.landmarks_mapping['user_name']]
            subject_id = row[m.landmarks_mapping['subject_ids']]
            subject_data = row[m.landmarks_mapping['subject_data']]
            filename = self.extract_filename(subject_data, subject_id,
                                             classification_id)
            annotations = row[m.landmarks_mapping['annotations']]
            annotation = self.extract_annotation(annotations, classification_id)

            if filename == '' or annotation == '':
                skipped_counter += 1
                continue

            raw_collection.add_subject(subject_id, filename, classification_id,
                                       annotation, annotator)
            processed_counter += 1
            print '\rCSV record %s (%d) is processed.' % (classification_id,
                                                          processed_counter),
                                                      

        print
        print 'Total records processed for the csv file: %d' % processed_counter
        print 'Total records skipped for the csv file: %d' % skipped_counter
        print 'Total subjects processed for the csv file: %d\n' % \
              len(raw_collection.get_subjects())
        csvfile.close()

        return raw_collection

    # extract filename from subject_data string.
    # subject_data string has the format:
    # {subject_id:{"retired": {...}, "Filename": "..."}}
    # For example:
    # {"20545611":{"retired":null,"Filename":"ESP_016715_2025_RED-0148.jpg"}}
    def extract_filename(self, subject_data_str, subject_id, classification_id):
        filename = ''
        json_obj = json.loads(subject_data_str)

        if not subject_id in json_obj:
            print 'CSV file internal inconsistence for the record with ' \
                  'classification id %s' % classification_id
            return filename
        subject_id_attr = json_obj[subject_id]

        if not 'Filename'  in subject_id_attr:
            print 'CSV file internal inconsistence for the record with ' \
                  'classification id %s' % classification_id
            return filename
        filename = subject_id_attr['Filename']

        return filename

    # extract annotation value from annotations string
    # annotations string has the format:
    # [{"task":xxx, "task_label": xxx, "value": xxx}]
    # For example:
    # [{"task":"T0","task_label":"Please select the landmark type","value":"other"}]
    def extract_annotation(self, annotations_str, classification_id):
        annotation_value = ''
        json_obj = json.loads(annotations_str)

        if len(json_obj) == 0:
            print 'CSV file internal inconsistence for the record with ' \
                  'classification id %s' % classification_id
            return annotation_value

        if not 'value' in json_obj[0]:
            print 'CSV file internal inconsistence for the record with ' \
                  'classification id %s' % classification_id
            return annotation_value
        annotation_value = json_obj[0]['value']

        return annotation_value

    # save subjects to a csv file named gold_standard.csv in out_dir directory.
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
            filename = subject.get_filename()
            records = subject.get_records()
            if not len(records) == 1:
                print 'Subject with subject_id=%s contains more than 1 record,' \
                      ' which is unexpected. Skipped.'
                continue
            annotation = records[0].get_annotation()

            csvwriter.writerow([subject_id, filename, annotation])
            #print 'Saved subject_id=%s, filename=%s, annotation=%s' % \
            #      (subject_id, filename, annotation)

        csvfile.close()

