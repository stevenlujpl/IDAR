# landmarks_crater_vs_other_rule.py
#
# Steven Lu 3/27/2019

import numpy as np
from rule.landmarks_rule import LandmarksRule

class LandmarksCraterVsOtherRule(LandmarksRule):
    def __init__(self, retirement_count):
        super(LandmarksCraterVsOtherRule, self).__init__(retirement_count)

    # defines the rules of ambiguous subjects
    def is_ambiguous(self, subject):
        records = subject.get_records()

        # subject doesn't go to ambiguous list if it is not retired yet.
        if len(records) < self._retirement_count:
            return False

        annotations = [r.get_annotation() for r in records]
        votes = np.unique(annotations)

        if len(votes) == 1:
            return False
        elif 'crater' in votes and 'other' in votes:
            return True
        else:
            return False
