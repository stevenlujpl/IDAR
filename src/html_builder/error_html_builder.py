# error_html_builder.py
# Builds a static HTML page for image error analysis
#
# Steven Lu 1/10/2019

from html_builder.landmarks_html_builder import LandmarksHTMLBuilder

class ErrorHTMLBuilder(LandmarksHTMLBuilder):
    def __init__(self, image_dir, template_dir, out_dir):
        super(ErrorHTMLBuilder, self).__init__(image_dir, template_dir, out_dir)

        # Overwrite parent's attributes
        self._template_name = 'error-analysis.tmpl'
        self._sub_dir = 'misclassified-subjects'
        self._html_name = 'error-analysis.html'
