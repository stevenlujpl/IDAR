# ambiguous_collection.py
# Mangaing ambiguous subjects
#
# Steven Lu 4/23/2018

from entity.subject import Subject

class AmbiguousCollection:
    def __init__(self, subjectList):
        if subjectList != None:
            self._subjects = subjectList
        else:
            self._subjects = []

    def get_subjects(self):
        return self._subjects

    def set_subjects(self, subjectList):
        self._subjects = subjectList

    def add_subject(self, subject):
        self._subjects.append(subject)

    def build_html(self, html_builder):
        html_builder.build(self._subjects)
