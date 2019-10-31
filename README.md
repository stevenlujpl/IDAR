## Interactive Data Analyzer and Reviewer (IDAR) for Machine Learning Systems 

IDAR is a tool written in Python, Javascript, HTML5, and CSS. 

It provides functionalities to help analyze ambiguous subjects/labels. It takes a raw CSV file exported from [Zooniverse](https://www.zooniverse.org/) as input, and categorizes the records in the CSV file into "gold standard" and "ambiguous" categories. The records in "gold standard" category will be saved as gold_standard.csv in specified output directory, and the records in "ambiguous" category will be used to construct a static HTML page for further analysis. 

It currently only supports CSV file exported from Zooniverse, but it can be extended to support other format. The rules for determining whether an image goes into "gold standard" and "ambiguous" can be customized. For adapting it to use for other projects, please read Extension and Adaptation section.

### Dependency
* Python dependencies: 
  + numpy
  + Cheetah --- it is an open source template engine and code-generation tool.
  
* HTML5/Javascript dependencies:
  + A browser that supports HTML5 [Web Storage](https://www.w3schools.com/html/html5_webstorage.asp) and [Download Attribute](https://webdesign.tutsplus.com/tutorials/quick-tip-using-the-html5-download-attribute--cms-23880).
  + Google Chrome is recommended. The Javascript/HTML/CSS code should work on most of browsers (e.g. chrome, safari, firefox, IE) updated to recent versions. However, the code is not tested on browsers other than Google Chrome. 
  + Be sure to enable third-party cookies in your browser. The HTML/Javascript code uses [web storage](https://en.wikipedia.org/wiki/Web_storage), and it will be disabled if cookie is disabled.

### Usages

#### ALA Usage
Use the following command to generate a static HTML page for analyzing "ambiguous" subjects, and it will also generate a "gold standard" csv file.

`python ambiguous_label_analyzer.py image_dir input_csv template_dir output_dir`

Where image_dir is a directory that contains all of the images; input_csv is the csv file exported from Zooniverse; template_dir is a directory that contains the HTML template files (.tmpl); output_dir is the output directory that contains the static "ambiguous" HTML page and the "gold standard" csv file.

For example: 

`python ambiguous_label_analyzer.py /Users/youlu/Desktop/PDS_image_classification/salience_experiments/cropped_images/ ../test/input/mars-landmarks-classifications-2018-04-24.csv templates/ ../test/output/`

#### OIA Usage:
You can also generate an HTML page to review outliers (given feature vectors
in your chosen representation).

`python outlier_image_analyzer.py image_dir feature_file template_dir output_dir`

e.g.

`python outlier_image_analyzer.py ~/Research/DEMUD/results/mislabeled/landmarks-v2/v2/5 ~/Research/DEMUD/DEMUD-github/scripts/cnn_feat_extraction/feats/v2fc6-class5.csv templates/ class5`

In this case, the feature vectors were extracted for class 5 from the AlexNet CNN.  See 

https://github.com/wkiri/DEMUD/tree/master/scripts/cnn_feat_extraction

for instructions on how to extract these feature vectors.

#### EAT Usage:
You can also generate an HTML page to review mis-classified images.

`python error_analyzer.py image_dir label_file pred_file template_dir output_dir classmap_file -n=integer`

e.g.

`python error_analyzer.py ~/PDS_image_classification/images/ ~/COSMIC/working_dir/eat_v1.1.0_2019_3_14/labels-val.txt ~/COSMIC/working_dir/eat_v1.1.0_2019_3_14/preds-val.txt templates/ ~/COSMIC/working_dir/eat_v1.1.0_2019_3_14/output ~/COSMIC/working_dir/eat_v1.1.0_2019_3_14/classmap.txt -n=200`

Note that `classmap_file` and `-n` arguments are optional.

### Logging

The tool doesn't provide a parameter to save a log file, instead, the python code uses `print` statement to write to `stdout`, so one can redirect the `stdout` to a file for logging purposes. See the following example,

`python ambiguous_label_analyzer.py /Users/youlu/Desktop/PDS_image_classification/salience_experiments/cropped_images/ ../test/input/mars-landmarks-classifications-2018-04-24.csv templates/ ../test/output/ > ../test/log.txt`

### Design
![class diagram and flow diagram](https://github.com/youlu860612/IDAR/blob/master/design.jpg)

### Extension and Adaptation

The tool is designed and modularized so that it is relatively easy to be adapted by other projects. In order to use this tool for other projects, you need to make the following changes to the code (the modules highlighted in green in the above diagram).
* create a script similar to [landmarks_csv_parser.py](https://github.com/youlu860612/IDAR/blob/master/src/parser/landmarks_csv_parser.py), and implement the `parse()` and `save()` functions.
* create a script similar to [landmarks_rule.py](https://github.com/youlu860612/IDAR/blob/master/src/rule/landmarks_rule.py), and implement the `is_gold_standard()` and `is_ambiguous()` functions.
* create a script similar to [landmarks_html_builder.py](https://github.com/youlu860612/IDAR/blob/master/src/html_builder/landmarks_html_builder.py), and implement the `build()` function.
* create a HTML template file similar to [landmarks.tmpl](https://github.com/youlu860612/IDAR/blob/master/src/templates/landmarks.tmpl).
* create a main script similar to [ambiguous_label_analyzer.py](https://github.com/youlu860612/IDAR/blob/master/src/ambiguous_label_analyzer.py).

<!--
 LocalWords:  Javascript CSV Zooniverse csv numpy firefox IE py dir tmpl CNN
 LocalWords:  outlier AlexNet stdout html
-->


### Copyright

Copyright (c) 2019, California Institute of Technology ("Caltech"). U.S. Government sponsorship acknowledged.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
*  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of Caltech nor its operating division, the Jet Propulsion Laboratory, nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

