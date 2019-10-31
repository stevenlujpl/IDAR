# cd_list_parser.py
# "cd" stands for class discovery. This scripts parses the input list file into
# collection object.
#
# Steven Lu 5/20/2019

from collection.cd_raw_collection import CDRawCollection


class CDListParser:
    # #########################################################
    # Example label file format:
    # 2030ML0107160000800325E01_DRCL.jpg
    # 1001ML0044510000305256D01_DRCL.jpg
    # ...
    # 0549ML0022160040204128E01_DRCL.jpg
    # 0078ML0005810000102763E01_DRCL.jpg
    # #########################################################
    def __init__(self, list_path):
        self._list_path = list_path

    def get_list_path(self):
        return self._list_path

    def set_list_path(self, list_path):
        self._list_path = list_path

    def parse(self):
        list_file = open(self._list_path, 'r')
        list_lines = list_file.readlines()

        raw_collection = CDRawCollection([])
        for l in list_lines:
            raw_collection.add_subject(l.rstrip())

        list_file.close()

        return raw_collection