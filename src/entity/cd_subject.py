# cd_subject.py
# An entity class contains attribute image_name.
#
# Steven Lu 5/20/2019


class CDSubject:
    def __init__(self, image_name):
        self._id = image_name
        self._filename = image_name

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_filename(self):
        return self._filename

    def set_filename(self, filename):
        self._filename = filename
