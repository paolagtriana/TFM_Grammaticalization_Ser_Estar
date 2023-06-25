'''IMPORTANT:  This script is continuing what has been done with separator.py
    The files that will be analyzed need to be in a folder (in this case, called 'corpus')
    and each of them will be in a subfolder (A, B, C, D, E) depending on its name.'''

''' IMPORTING PACKAGES '''
# To use this program, it is required to have Python and Pip installed
# To install BS, the following line will be executed in terminal: pip install beautifulsoup4
import os
import pandas as pd
from collections import Counter
import numpy as np
import math
from bs4 import BeautifulSoup as BS

'''LOADING THE DATA'''
#Creation of a list of the paths of the files to analyze
corpuspaths = ['./corpus/A/', './corpus/B/', './corpus/C/', './corpus/D/', './corpus/E/']

''' PROCESSING THE DATA '''
print("\n")
#We set the interval that we want for our bins
bin_size = int(input('Which size do you want the bins to be?: '))
#We create a list of periods using our bin size adding it to the ending point,
#To make sure that the last element is included even if the last period is not a divisor of our bin size
bins = np.arange(1100, 1599 + bin_size, bin_size).tolist()

#We create a loop for iterating through every element of the list of paths created above
for path in corpuspaths:
    #We list the name of all TXT files of each folder (and exclude the hidden items)
    files = [f for f in os.listdir(path) if f.endswith('.txt') and not f.startswith('.')]
    #We sort the obtained lits
    files.sort(key=lambda x: '{0:0>8}'.format(x).lower())
    
    #We create a loop for iterating through every file in each folder
    for file in files:
        #We open the file to be analyzed by defining its path and indicating the encoding
        corpus = open(path + file, encoding='UTF-8')
        
        #We apply the BS model to our file with BS(), BeautifulSoup is used for web scrapping and is suitable for our type of metadata
        soup = BS(corpus)
        
        #We search for the content of every label that coincides with the given string 'text'
        elem = soup.findAll('text')
        '''The purpose of the soup.findAll() step is to separate each text
        and save them as separate elements in a list, since every text is
        inserted between <text></text> and the metadata is included by giving attributes
        to that label (for example, 'author=' or 'date=''are both attributes of <text>)'''
        
        #We separate the content of the label
        text = elem[0].text.split()
        
        #We create an empty list for saving all the information of each wordform
        tokens_lemmas_labels = []
        
        #We create a variable and assign it to the length of the text
        i = len(text)
        #We create a loop that iterates through every 3 elements and store them in a dict format until the text is empty
        while i != 0:
            tokens_lemmas_labels.append({"Token":text[0], "Lemma":text[1], "Label":text[2]})
            #We delete the items that have just been stored
            del text[0:3]
            #We reassign the variable 'i' to adjust to the new length of the text
            i = len(text)
        
        #We create a dataframe with the dictionary created above
        df = pd.DataFrame({'Token': [x['Token'] for x in tokens_lemmas_labels],
                            'Lemma': [x['Lemma'] for x in tokens_lemmas_labels],
                            'Label': [x['Label'] for x in tokens_lemmas_labels]})
            
        #We search for the attribute of the label <text> called 'date' and assign it to a variable
        date = int(elem[0]['date'])
        
        #We assing a period to the file depending on its date
        #We remove the origin date such that 0 = 1100
        temp = date - 1100
        #We find out how many units of our interval we have (that is, how many bins)
        temp = temp/bin_size
        #We use math.floor() in case we have obtained a floating number
        temp = math.floor(temp)
        #We use the number we have obtained to indicate the index of th date in the list of bins
        mybin = bins[temp]
        
        #We create a new folder called 'csv_{bin_size}_years' and a subfolder for the current bin in case it does not exist already
        path_folder = "./corpus/csv_" + str(bin_size) + "_years/"
        
        try:
            os.makedirs(path_folder + str(mybin) + "/")
        except FileExistsError: # directory already exists
            pass
        
        df.to_csv(path_folder + str(mybin) + "/" + file.replace('.txt', '.csv'), index=False)

        #OPTIONAL: The script prints the file that has just been analized as a control measure
        print(f'File {file} done')
