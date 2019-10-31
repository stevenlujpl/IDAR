# raw_collection.py
# Represents the raw csv file.
#
# Steven Lu 4/20/2018

from entity.subject import Subject

class RawCollection(object):
    def __init__(self, subjectList):
        if subjectList != None:
            self._subjects = subjectList
        else:
            self._subjects = []

    def get_subjects(self):
        return self._subjects

    def set_subjects(self, subjectList):
        self._subjects = subjectList

    # Add a subject to raw collection. The method will handle duplicates
    # accordingly, so no need to check whether or not a subject is a duplicate
    # in the caller of this method.
    def add_subject(self, subject_id, filename, classification_id, annotation,
                    annotator):
        is_subject_exist, subject = self.is_subject_exist(subject_id)
        if is_subject_exist:
            # if subject exists, merge the record to the existing subject
            subject.add_record(classification_id, annotation, annotator)
        else:
            # if subject doesn't exist, add a record and attach it to a new
            # subject.
            subject = Subject(subject_id, filename)
            subject.add_record(classification_id, annotation, annotator)
            self._subjects.append(subject)

    # The function returns a boolean that indicates whether or not the subject
    # exists. If it exists, then return the subject object to the caller.
    def is_subject_exist(self, subject_id):
        for subject in self._subjects:
            if subject.get_subject_id() == subject_id:
                return True, subject
        return False, None

