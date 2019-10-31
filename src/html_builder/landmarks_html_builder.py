# landmarks_html_builder.py
# Builds a static HTML page for analyzing ambiguous subjects
#
# Steven Lu 4/24/2018

import os
import errno
import datetime
from shutil import copyfile, copytree, rmtree
from Cheetah.Template import Template


class LandmarksHTMLBuilder(object):
    def __init__(self, image_dir, template_dir, out_dir):
        self._image_dir = image_dir
        self._template_dir = template_dir
        self._template_name = 'landmarks.tmpl'
        self._out_dir = out_dir
        self._sub_dir = 'ambiguous_subjects'
        self._html_name = 'landmarks.html'

    def get_image_dir(self):
        return self._image_dir

    def set_image_dir(self, image_dir):
        self._image_dir = image_dir

    def get_template_dir(self):
        return self._template_dir

    def set_template_dir(self, template_dir):
        self._template_dir = template_dir

    def get_out_dir(self):
        return self._out_dir

    def set_out_dir(self, out_dir):
        self._out_dir = out_dir

    def build(self, subjects):
        template_file = '%s/%s' % (os.path.abspath(self._template_dir),
                                   self._template_name)
        print 'Building an HTML page %s/%s' % \
              (os.path.abspath(self._out_dir), self._html_name)
        print 'Template file: %s' % os.path.abspath(template_file)

        if not os.path.isfile(template_file):
            print '%s template file does not exist. Cannot build HTML page ' \
                  'for analyzing ambiguous subjects.'
            return

        # if output directory doesn't exist, create it.
        if not os.path.isdir(self._out_dir):
            print 'Create output directory %s' % self._out_dir
            try:
                os.makedirs(self._out_dir)
            except OSError:
                if OSError.errno == errno.EEXIST and \
                        os.path.isdir(self._out_dir):
                    pass
                else:
                    raise

        # create a sub directory for storing all ambiguous subjects if it
        # doesn't already exist.
        sub_dir_path = '%s/%s' % (self._out_dir, self._sub_dir)
        if not os.path.isdir(sub_dir_path):
            try:
                os.makedirs(sub_dir_path)
            except OSError:
                if OSError.errno == errno.EEXIST and os.path.isdir(sub_dir_path):
                    pass
                else:
                    raise

        # copy the ambiguous subjects from image_dir to a sub directory in
        # output_dir.
        print 'Copying subjects from input to output directory.'
        for subject in subjects:
            file_path = '%s/%s' % (self._image_dir, subject.get_filename())
            if not os.path.isfile(file_path):
                print 'Failed copying subject %s because it does not exist in ' \
                      'image_dir.' % file_path
                continue
            copyfile(file_path, '%s/%s/%s' % (self._out_dir, self._sub_dir,
                                              subject.get_filename()))

        # copy the libs directory into output directory
        src_libs_path = '%s/%s' % (self._template_dir, 'libs')
        des_libs_path = '%s/%s' % (self._out_dir, 'libs')
        # copytree() dies on mkdir() if the subdirs already exist
        # in the destination directory.  So let's clear them out first.
        if os.path.isdir(des_libs_path):
            rmtree(des_libs_path)
        copytree(src_libs_path, des_libs_path)

        # generate a unique-ish identifier to be used as part of the keys for 
        # HTML's local strorage
        now = datetime.datetime.now()
        identifier = '%s%s%s^' % (now.hour, now.minute, now.second)

        # build the web page
        template = Template(file=template_file, searchList=[{
            'sub_dir': self._sub_dir,
            'subjects': subjects,
            'total': len(subjects),
            'identifier': identifier
        }])
        with open('%s/%s' % (self._out_dir, self._html_name), 'w+') as f:
            f.write(str(template))
