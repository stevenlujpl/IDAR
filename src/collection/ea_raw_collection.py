# ea_raw_collection.py
# "ea" stands for error analysis. This script is used by error analysis related
# scripts, and represents a raw csv file.
# 
# Steven Lu 1/9/2019

from entity.ea_subject import EASubject
from collection.raw_collection import RawCollection

class EARawCollection(RawCollection):
    def __init__(self, subject_list):
        super(EARawCollection, self).__init__(subject_list)

    # Overwrite parent's add_subject() function
    def add_subject(self, id, label, pred, conf):
        subject = EASubject(id, label, pred, conf)
        self._subjects.append(subject)
