# all imports
from os import path
from psychopy import gui
import pandas as pd
from unidecode import unidecode  # for convertion czech symbols to english ones


# read xls table with all images names from all subjects
all_names = pd.read_excel('f:\Sofia\sleep project\EMT study\ALL_results\PsychoPy xls\image names\ALL_GOOD\All_names_of_images.xlsx')
all_names = all_names.set_index('sound')

# delete unnessesary columns
all_names.drop(columns=['image', 'set'], inplace=True)

# convert all czech symbols to english symbols and make all lower case
for column in all_names.columns:
  all_names[column] = all_names[column].apply(lambda x: unidecode(x.lower()))


# Function to remove duplicates in a row
def remove_duplicates(row):
    seen = set()
    unique_values = []
    for value in row:
        if value not in seen:
            unique_values.append(value)
            seen.add(value)
    return unique_values


# apply the function to each row in the DataFrame
all_unique_names = all_names.apply(remove_duplicates, axis=1)


# a function to check if the answer is in the list within the all_unique_names series
def check_answer(row):
    sound_name = row['sound_free_recall']
    answer = row['answer']
    if sound_name in all_unique_names.index:
        names_set = all_unique_names[sound_name]
        return 1 if answer in names_set else answer
    else:
        return answer


# upload the files for all subjects (free recall before and after sleep)
filenames = gui.fileOpenDlg(allowed="*.xlsx")

# create an empty DataFrame to store the aggregated data
aggregated_data = pd.DataFrame()

for thisFilename in filenames:
    # read xls file
    df = pd.read_excel(thisFilename)

    file_parts = path.splitext(path.basename(thisFilename))[0].split('_')
    subject_id = file_parts[0]
    sleep_status = file_parts[3]  # before or after sleep

    # leave only nessesary columns
    df_new = df[['sound_free_recall', 'answer']]

    # convert all czech symbols to english symbols and make all lower case
    df_new['answer'] = df_new['answer'].apply(lambda x: unidecode(x.lower()) if isinstance(x, str) else x)

    # apply the function to each row in the DataFrame to check if the answer is correct
    df_new['answer'] = df_new.apply(check_answer, axis=1)

    # set the 'sound_free_recall' column as the index
    df_new.set_index('sound_free_recall', inplace=True)

    # rename the 'answer' column to 'before_sleep' or 'after_sleep' based on sleep status
    df_new.rename(columns={'answer': f'{sleep_status}_sleep'}, inplace=True)

    # transpose the DataFrame to have sounds as columns
    df_new = df_new.T

    # add the 'subject_id' as a new column
    df_new['subject_id'] = subject_id

    # append the subject's data to the aggregated DataFrame
    aggregated_data = pd.concat([aggregated_data, df_new], axis=0)

# reset the index
aggregated_data.reset_index(drop=True, inplace=True)

# set the index to 'subject_id' to create two levels of subcolumns
aggregated_data.set_index(['subject_id', ['after_sleep', 'before_sleep'] * (len(aggregated_data) // 2)], inplace=True)

# reset the index levels for the final structure
aggregated_data.index.names = ['subject_id', '']

# export a final table to xls
file_name = "\Free_recall_aggregated_table.xlsx"
aggregated_data.to_excel('f:\Sofia\sleep project\EMT study\ALL_results\PsychoPy xls' + file_name)



