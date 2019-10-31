# ea_subject.py
# An entiry class contains attributes id, label, prediction, confidence score
# 
# Steven Lu 1/9/2019

class EASubject:
    def __init__(self, id, label, pred, conf):
        self._id = id         # ID of the image
        self._label = label   # Label of the image
        self._pred = pred     # Predicted label of the image
        self._conf = conf     # Confidence score of the prediction
        self._filename = id    # The filename of the image

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_label(self):
        return self._label

    def set_label(self, label):
        self._label = label

    def get_pred(self):
        return self._pred

    def set_pred(self, pred):
        self._pred = pred

    def get_conf(self):
        return self._conf

    def set_conf(self, conf):
        self._conf = conf

    def get_filename(self):
        return self._filename

    def set_filename(self, filename):
        self._filename = filename
