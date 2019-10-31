# landmarks_slopestreak_vs_other_rule.py
#
# Steven Lu 5/13/2019

import numpy as np
from rule.landmarks_rule import LandmarksRule


class LandmarksSlopestreakVsOtherRule(LandmarksRule):
    def __init__(self, retirement_count):
        super(LandmarksSlopestreakVsOtherRule, self).__init__(retirement_count)

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
        elif 'slope streak' in votes and 'other' in votes:
            return True
        elif 'slope streak' in votes and 'crater' in votes:
            return True
        else:
            return False
