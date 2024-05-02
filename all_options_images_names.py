# script to join all tables with all possible names of images across participants in one large table

# all imports
from os import path
from psychopy import gui
import pandas as pd

# Define a file path to the table with pairs of sounds and images
pairs_sounds_path = 'f:/Sofia/sleep project/EMT study/ALL_results/PsychoPy xls/image names/pair of sounds and images.xlsx'

# upload the files
filenames = gui.fileOpenDlg(allowed="*list_images_names*.xlsx")  # select all xls files with filename _list_images_names
ind = 0  # index for column names
dfs = []  # for all tables

for thisFilename in filenames:
    print(thisFilename)
    ind += 1
    # read xls file
    df = pd.read_excel(thisFilename)
    df = df.drop(df.columns[0], axis=1)  # delete redundant column
    # set column with image names as an index
    df = df.set_index('image2name')
    df = df.rename(columns={'image2name': 'image', 'name': 'name' + str(ind)})
    dfs.append(df)  # save all tables in one list

# join all tables in one
output = dfs[0].join(dfs[1:])

# add table with pairs of sounds and images
pairs = pd.read_excel(pairs_sounds_path)
pairs = pairs.set_index('image')
#print(pairs)
output = pairs.join(output)

# export to xls
output_folder = path.dirname(path.abspath(thisFilename))
file_name = "all_names_of_images.xlsx"
output.to_excel(output_folder+"/"+file_name)
print(f'{file_name} is written to Excel File successfully.')
