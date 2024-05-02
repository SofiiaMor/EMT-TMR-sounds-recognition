# script for exporting data from psychopy test after sleep to Excel file; output - 2 xls files per participant -
# free recall and image names table

# all imports
from os import path
from psychopy import gui
import pandas as pd

# upload the files
filenames = gui.fileOpenDlg(allowed="*.csv") # select csv files from the morning session for the all participants we need

for thisFilename in filenames:
    print(thisFilename)
    df = pd.read_csv(thisFilename)
    # view the dataset
    pd.set_option('display.max_columns', None)
    #print(df.head())

    # convert date
    df['date'] = df['date'][0].split('.')[0]

    # select only important columns
    free_recall = df[['sound_free_recall', 'set', 'textbox.text', 'textbox.started']]
    image_names = df[['image2name', 'textbox_image.text']]

    # remove rows with NaN
    image_names = image_names.dropna(how='all').reset_index(drop=True)
    free_recall = free_recall.dropna(how='all').reset_index(drop=True)

    # clean text responses from \n
    free_recall['textbox.text'] = free_recall['textbox.text'].str.replace('\n', '')
    image_names['textbox_image.text'] = image_names['textbox_image.text'].str.replace('\n', '')

    # rename columns
    image_names = image_names.rename(columns={'textbox_image.text': 'name'})
    free_recall = free_recall.rename(columns={'textbox.text': 'answer', 'textbox.started': 'sound_start'})
    free_recall['time_exp'] = ' '  # add date and time of the experiment to the table
    free_recall.at[0, 'time_exp'] = df['date'][0]

    # export to xls
    output_folder = path.dirname(path.abspath(thisFilename))
    list_name = [df['participant'][0], 'list_images_names', df['date'][0]]
    file_name = "_".join(list_name) + ".xlsx"
    image_names.to_excel(output_folder+"/"+file_name)
    print(f'{file_name} is written to Excel File successfully.')
    
    #  free_recall table
    list_name2 = [df['participant'][0], 'free_recall_after_sleep', df['date'][0]]
    file_name2 = "_".join(list_name2) + ".xlsx"
    free_recall.to_excel(output_folder+"/"+file_name2)
    print(f'{file_name2} is written to Excel File successfully.')
