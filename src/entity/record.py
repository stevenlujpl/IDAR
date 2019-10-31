# record.py
# An entity class that represents certain fields in a row of the master csv
# file, and it contains the following attributes:
# * annotation --- the classification result
# * annotator --- username for the person who added this annotation
#
# Steven Lu 4/20/2018

class Record:
    def __init__(self, classification_id, annotation, annotator):
        self._classification_id = classification_id  # classification id
        self._annotation = annotation
        self._annotator = annotator

    def get_classification_id(self):
        return self._classification_id

    def set_classification_id(self, classification_id):
        self._classification_id = classification_id

    def get_annotation(self):
        return self._annotation

    def set_annotation(self, annotation):
        self._annotation = annotation

    def get_annotator(self):
        return self._annotator

    def set_annotator(self, annotator):
        self._annotator = annotator

