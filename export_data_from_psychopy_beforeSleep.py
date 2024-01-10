# script for exporting data from psychopy test before sleep to Excel file; output - 2 xls files per participant -
# forced choice and free recall

# all imports
from os import path
from psychopy import gui
import pandas as pd

# upload the files
filenames = gui.fileOpenDlg(allowed="*.csv")  # select csv files for the all participants we need

for thisFilename in filenames:
    print(thisFilename)
    df = pd.read_csv(thisFilename)
    # view the dataset
    pd.set_option('display.max_columns', None)
    #print(df.head())

    # convert date
    df['date'] = df['date'][0].split('.')[0]

    # select only important columns
    forced_choice = df[['image_left', 'image_right', 'image_up', 'image_down', 'sound', 'corrans', 'condition',
                        'key_resp.keys', 'key_resp.corr', 'key_resp.rt', 'sound_test.started', 'image_R.started']]
    free_recall = df[['sound_free_recall', 'set', 'textbox.text', 'textbox.started']]

    # remove rows with NaN
    forced_choice = forced_choice.dropna(how='all').reset_index(drop=True)
    free_recall = free_recall.dropna(how='all').reset_index(drop=True)

    # compute true RT decreased by time from the start of image presentation to the start of sound presenting
    forced_choice['key_resp.rt'] = forced_choice['key_resp.rt'] - (forced_choice['sound_test.started'] - forced_choice['image_R.started'])
    forced_choice = forced_choice.drop(columns={'sound_test.started', 'image_R.started'})  # delete redundant columns
    forced_choice['time_exp'] = ' '  # add date and time of the experiment to the table
    forced_choice.at[0, 'time_exp'] = df['date'][0]

    # clean text responses from \n
    free_recall['textbox.text'] = free_recall['textbox.text'].str.replace('\n', '')

    # rename columns
    free_recall = free_recall.rename(columns={'textbox.text': 'answer', 'textbox.started': 'sound_start'})
    free_recall['time_exp'] = ' '  # add date and time of the experiment to the table
    free_recall.at[0, 'time_exp'] = df['date'][0]

    # export to xls
    # the name of the file of forced_choice table
    output_folder = path.dirname(path.abspath(thisFilename))
    list_name = [df['participant'][0], 'forced_choice',  df['date'][0]]
    file_name = "_".join(list_name) + ".xlsx"
    forced_choice.to_excel(output_folder+"/"+file_name)
    print(f'{file_name} is written to Excel File successfully.')
    
    # another free_recall table
    list_name2 = [df['participant'][0], 'free_recall_before_sleep', df['date'][0]]
    file_name2 = "_".join(list_name2) + ".xlsx"
    free_recall.to_excel(output_folder+"/"+file_name2)
    print(f'{file_name2} is written to Excel File successfully.')
