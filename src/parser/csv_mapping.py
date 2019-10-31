#csv_mapping.py
# Provides the column title and column indices mapping for csv files.
#
# Steven Lu 4/23/2018
# History:
# Steven Lu 1/9/2019 add class mapping for landmarks v3 dataset 

landmarks_is_title_first_row = True
landmarks_mapping = {
    'classification_id': 0,
    'user_name': 1,
    'user_id': 2,
    'user_ip': 3,
    'workflow_id': 4,
    'workflow_name': 5,
    'workflow_version': 6,
    'created_at': 7,
    'gold_standard': 8,
    'expert': 9,
    'metadata': 10,
    'annotations': 11,
    'subject_data': 12,
    'subject_ids': 13
}
