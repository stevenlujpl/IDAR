# cd_html_builder.py
# Builds a static HTML page for class discovery.
#
# Steven Lu 5/20/2019

from html_builder.landmarks_html_builder import LandmarksHTMLBuilder


class CDHtmlBuilder(LandmarksHTMLBuilder):
    def __init__(self, image_dir, template_dir, out_dir):
        super(CDHtmlBuilder, self).__init__(image_dir, template_dir, out_dir)

        # Overwrite parent's attributes
        self._template_name = 'class-discovery.tmpl'
        self._sub_dir = 'images'
        self._html_name = 'class-discovery.html'
