# gold_standard_collection.py
# Managing gold standard subjects
#
# Steven Lu 4/23/2018

from entity.subject import Subject

class GoldStandardCollection:
    def __init__(self, subjectList):
        if subjectList != None:
            self._subjects = subjectList
        else:
            self._subjects = []

    def get_subjects(self):
        return self._subjects

    def set_subjects(self, subjectList):
        self._subjects = subjectList

    def add_subject(self, subject, annotation):
        gold_standard_subject = Subject(subject.get_subject_id(),
                                        subject.get_filename())
        gold_standard_subject.add_record('', annotation, '')
        self._subjects.append(gold_standard_subject)
        #print 'Add to gold standard collection: subject_id=%s, filename=%s, ' \
        #      'annotation=%s' % (subject.get_subject_id(), subject.get_filename(),
        #                         annotation)

    def save_csv(self, csvparser):
        csvparser.save(self._subjects)
