# Usage
Here's the order how you should use the scripts:
1. run `export_data_from_psychopy_beforeSleep.py` to export the data from the psychopy file before sleep to Excel files; 
    - output - 2 xls files per participant - forced choice and free recall
2. run `export_data_from_psychopy_afterSleep.py` to export the data from the psychopy file after sleep to Excel files; 
    - output - 2 xls files per participant - free recall and image names table
3. run `forced_choice_summary.py` to get summary of the forced choice task of all subjects; 
    - output - 1 xls table: N of correct answers, accuracy and mean RT for each subject
4. run `all_options_images_names.py` to join all tables with all possible names of images across participants in one table; 
    - output - 1 xls file with all images names
5. run `create_large_table.py` to get aggregated table with all subjects' answers to free recall task before and after sleep;
   - 1 indicates that the answer is correct, empty cell - no response was given, otherwise the original word given by the subject is written
