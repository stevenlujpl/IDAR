# subject.py
# An entity class that contains a list of records.
#
# Steven Lu 4/20/2018

from record import Record

class Subject:
    def __init__(self, subject_id, filename):
        self._subject_id = subject_id               # subject id
        self._filename = filename
        self._records = []

    def get_subject_id(self):
        return self._subject_id

    def set_subject_id(self, subject_id):
        self._subject_id = subject_id

    def get_filename(self):
        return self._filename

    def set_filename(self, filename):
        self._filename = filename

    def get_records(self):
        return self._records

    def set_records(self, records):
        self._records = records

    def add_record(self, classification_id, annotation, annotator):
        if not self.is_record_exist(classification_id):
            record = Record(classification_id, annotation, annotator)
            self._records.append(record)

    def is_record_exist(self, classification_id):
        # check duplicate record.
        for record in self._records:
            if record.get_classification_id() == classification_id:
                print 'Duplicate record found. Classification id is %s. Skip ' \
                      'the duplicate record.' % classification_id
                return True

        return False
