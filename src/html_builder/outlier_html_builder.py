# outlier_html_builder.py
# Builds a static HTML page for reviewing outliers
#
# Steven Lu 4/24/2018
# Kiri Wagstaff 8/15/2018

from Cheetah.Template import Template

import os
import errno
from shutil import copyfile
from landmarks_html_builder import LandmarksHTMLBuilder

class OutlierHTMLBuilder(LandmarksHTMLBuilder):
    def __init__(self, image_dir, template_dir, out_dir):
        self._image_dir = image_dir
        self._template_dir = template_dir
        self._template_name = 'outlier.tmpl'
        self._out_dir = out_dir
        self._sub_dir = 'ambiguous_subjects'
        self._html_name = 'outlier.html'

