# script to create a summary of the forced choice task of all subjects
# output - N of correct answers, accuracy and mean RT for each subject

# all imports
from os import path
from psychopy import gui
import pandas as pd
import numpy as np

# upload the prepared files with name forced_choice
filenames = gui.fileOpenDlg(allowed="*forced_choice*.xlsx")

# output table with all subjects
output = []
columns_name = ('subject', 'n_corr_sounds', 'accuracy', 'mean_RT_sec')

# go through all xls files
for thisFilename in filenames:
    # read xls file
    df = pd.read_excel(thisFilename)
    file_parts = path.splitext(path.basename(thisFilename))[0].split('_')
    subject_id = file_parts[0]
    # accuracy
    accuracy = df['key_resp.corr'].sum() / len(df['key_resp.corr']) * 100
    n_corr_sounds = df['key_resp.corr'].sum()
    # mean RT
    rt = df['key_resp.rt'].mean()

    # add all data in row
    output.append((subject_id, n_corr_sounds, accuracy, rt))

# create dataframe from all data
final_df = pd.DataFrame(output, columns=columns_name)
final_df.index = np.arange(1, len(final_df) + 1)  # change index starting from 1

# export to xls
output_folder = path.dirname(path.abspath(thisFilename))
file_name = 'forced_choice_overview.xlsx'
final_df.to_excel(output_folder + "/" + file_name)

print('DataFrame is written to Excel File successfully.')
