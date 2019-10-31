# msl_v2_rule.py
# Defines the rules for gold standard and ambiguous subjects for msl v2 labels
#
# Steven Lu 8/21/2019

import numpy as np


class MSLV2Rule(object):
    def __init__(self, retirement_count):
        if retirement_count % 2 == 0 and retirement_count < 3:
            raise ValueError('retirement count must be an odd number that is '
                             'greater than or equal to 3 to apply marjority '
                             'rule.')
        self._retirement_count = retirement_count

    def get_retirement_count(self):
        return self._retirement_count

    def set_retirement_count(self, retirement_couont):
        self._retirement_count = retirement_couont

    def is_gold_standard(self, subject):
        records = subject.get_records()

        # subject doesn't go to gold standard list if it is not retired yet.
        if len(records) < self._retirement_count:
            return False

        annotations = [r.get_annotation() for r in records]
        votes = np.unique(annotations)

        # all votes must agree to be considered gold standard subject
        if len(votes) == 1:
            return True
        else:
            return False

    def is_ambiguous(self, subject):
        records = subject.get_records()

        # subject doesn't go to ambiguous list if it is not retired yet.
        if len(records) < self._retirement_count:
            return False

        annotations = [r.get_annotation() for r in records]
        votes = np.unique(annotations)

        if len(votes) > 1:
            return True
        else:
            return False

    # extract gold standard annotation. In order to call this function, the
    # subject variable must be gold standard.
    def extract_gold_standard_annotation(self, subject):
        records = subject.get_records()
        annotations = [r.get_annotation() for r in records]

        if len(np.unique(annotations)) > 1:
            raise Exception('extract_gold_standard_annotation() should not be '
                            'used if the subject is not gold standard.')

        return annotations[0]
