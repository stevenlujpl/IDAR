# landmarks_rule.py
# Defines the rules for gold standard and ambigous subjects
#
# Steven Lu 4/23/2018

import numpy as np

class LandmarksRule(object):
    def __init__(self, retirement_count):
        if retirement_count % 2 == 0 and retirement_count < 3:
            raise ValueError('retirement count must be an odd number that is '
                             'greater than or equal to 3 to apply marjority '
                             'rule.')
        self._retirement_count = retirement_count
        self._valid_annotations = ['slope streak', 'crater', 'impact ejecta',
                                   'dark dune', 'bright dune', 'swiss cheese',
                                   'spider', 'other']

    def get_retirement_count(self):
        return self._retirement_count

    def set_retirement_count(self, retirement_couont):
        self._retirement_count = retirement_couont

    # defines the rules of gold standard subjects
    def is_gold_standard(self, subject):
        records = subject.get_records()

        # subject doesn't go to gold standard list if it is not retired yet.
        if len(records) < self._retirement_count:
            return False

        annotations = [r.get_annotation() for r in records]
        votes = np.unique(annotations)

        if len(votes) == 1:
            return True
        elif len(votes) == 2 and all(x in ['crater', 'other'] for x in votes):
            # with 2 different votes, and the votes are crater v.s. other
            return True
        else:
            return False

    # defines the rules of ambiguous subjects
    def is_ambiguous(self, subject):
        records = subject.get_records()

        # subject doesn't go to ambiguous list if it is not retired yet.
        if len(records) < self._retirement_count:
            return False

        annotations = [r.get_annotation() for r in records]
        votes = np.unique(annotations)

        if len(votes) == 3:
            return True
        elif len(votes) == 2 and not all(x in ['crater', 'other'] for x in votes):
            # with 2 different votes, and the votes are not crater v.s. other
            return True
        else:
            return False

    # extract gold standard annotation. In order to call this function, the
    # subject variable must be gold standard.
    def extract_gold_standard_annotation(self, subject):
        records = subject.get_records()
        annotations = [r.get_annotation() for r in records]
        votes = np.unique(annotations)

        if len(votes) == 1:
            return records[0].get_annotation()
        elif len(votes) == 2 and votes[0] in ['crater', 'other'] and \
            votes[1] in ['crater', 'other']:
                # this is hard coded logic based on the definition/discussion of
                # gold standard rules.
                if annotations.count('crater') >= annotations.count('other'):
                    return 'crater'
                else:
                    return 'other'
        else:
            # should never reach this branch
            return None
