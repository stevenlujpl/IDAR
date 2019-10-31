# cd_raw_collection.py
# "cd" stands for class discovery. This script is used by class discovery
# related scripts, and represents a raw input list file.
#
# Steven Lu 5/20/2019

from entity.cd_subject import CDSubject
from collection.raw_collection import RawCollection


class CDRawCollection(RawCollection):
    def __init__(self, subject_list):
        super(CDRawCollection, self).__init__(subject_list)

    # Overwrite parent's add_subject() function
    def add_subject(self, image_name):
        subject = CDSubject(image_name)
        self._subjects.append(subject)