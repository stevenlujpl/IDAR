# msl_v2_ambiguous_html_builder.py
# Builds a static HTML page for analyzing ambiguous subjects for msl v2 data set
#
# Steven Lu 8/21/2019

from html_builder.landmarks_html_builder import LandmarksHTMLBuilder


class MSLV2AmbiguousHTMLBuilder(LandmarksHTMLBuilder):
    def __init__(self, image_dir, template_dir, out_dir):
        super(MSLV2AmbiguousHTMLBuilder, self).__init__(image_dir, template_dir,
                                                        out_dir)

        # Overwrite parent's attributes
        self._template_name = 'msl-v2-ambiguous.tmpl'
        self._sub_dir = 'ambiguous-subjects'
        self._html_name = 'msl-v2-ambiguous.html'
