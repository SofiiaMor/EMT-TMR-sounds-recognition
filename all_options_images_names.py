# all imports 
from os import path
from psychopy import gui
import pandas as pd

# upload the files
filenames = gui.fileOpenDlg(allowed="*.xlsx")
ind = 0  # index for column names
dfs = []  # for all tables

for thisFilename in filenames:
    print(thisFilename)
    ind += 1
    # read xls file
    df = pd.read_excel(thisFilename)

    # set column with image names as an index
    df = df.set_index('image2name')
    df = df.rename(columns={'image2name': 'image', 'name': 'name' + str(ind)})
    dfs.append(df)  # save all tables in one list

# join all tables in one
output = dfs[0].join(dfs[1:])

# add table with pairs of sounds and images
pairs = pd.read_excel('f:/Sofia/sleep project/EMT study/all results/PsychoPy xls/image names/pair of sounds and images.xlsx')
pairs = pairs.set_index('image')
#print(pairs)
output = pairs.join(output)

# export to xls
output_folder = path.dirname(path.abspath(thisFilename))
file_name = "all_names_of_images.xlsx"
output.to_excel(output_folder+"/"+file_name)
print(f'{file_name} is written to Excel File successfully.')
