'''IMPORTANT:  This script is continuing what has been done with separator.py
    The files that will be split need to be in a folder (in this case, called 'corpus')
    and each of them will be in a subfolder (A, B, C, D, E) depending on its name.'''

''' IMPORTING PACKAGES '''
# To use this program, it is required to have Python and Pip installed
# To install BS, the following line will be executed in terminal: pip install beautifulsoup4
import os
import pandas as pd
from bs4 import BeautifulSoup as BS

''' LOADING THE DATA'''
#Creation of a list of the paths of the folders with the files to analyze
corpuspaths = ['./corpus/A/', './corpus/B/', './corpus/C/', './corpus/D/', './corpus/E/']

''' PROCESSING THE DATA '''
#We create empty lists with each attribute of the metadata
titles = []
authors = []
dates = []
centuries = []
collections = []
genres = []
ids = []
translations = []

#We create empty lists for storing the tokens and the types of all texts
all_tokens = []
all_types = []

#We create an empty list for storing the name of all files
all_files = []

for path in corpuspaths:
    #We list the name of all files in each subfolder
    subfolder = [f for f in os.listdir(path) if f.endswith('.txt') and not f.startswith('.')]
    #We sort the list
    subfolder.sort(key=lambda x: '{0:0>8}'.format(x).lower())
    
    #We create a loop for iterating through each file
    for file in subfolder:
        #We add the name of the current file being analyzed to the list of all file names
        all_files.append(file)
        
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
        
        #We search for every attribute of the label <text> and store them in separate lists
        titles.append(elem[0]['title'])
        authors.append(elem[0]['author'])
        dates.append(elem[0]['date'])
        centuries.append(elem[0]['century'])
        genres.append(elem[0]['genre'])
        ids.append(elem[0]['id'])
        translations.append(elem[0]['translation'])
        collections.append(elem[0]['collection'])
        tokens = []
        types = []
        
        #We separate the content of the label
        text = elem[0].text.split()
        #We create a variable and assign it to the length of the text
        i = len(text)
        
        #We create a loop that iterates through every 2 elements and store them in separate lists
        while i != 0:
            tokens.append(text[0])
            types.append(text[1])
            #We delete the items that have just been stored and the item that corresponds to the label
            del text[0:3]
            #We reassign the variable 'i' to adjust to the new length of the text
            i = len(text)
        
        #We add the tokens and types of the current file to the empty lists created above
        all_tokens.append(tokens)
        all_types.append(types)
        
        #OPTIONAL: The script prints the file that has just been analized as a control measure
        print(f'File {file} done')
        
        ''' FILTERING BY METADATA '''
        #We create our conditions
        # filter_condition = elem[0]['author'] == "Antonio de Nebrija" #The text was written by Antonio de Nebrija
        # filter_condition = int(elem[0]['date']) < 1400 #The text was produced before the year 1400
        # filter_condition = int(elem[0]['century']) < 15 #The text was produced before the 15th century
        # filter_condition = elem[0]['genre'] in ['poetry', 'prose'] #The is tagged as either poetry or prose
        # filter_condition = re.search(r'LA.', elem[0]['id']) #The text identifier contains the string 'LA'
        # filter_condition = elem[0]['translation'] == "YES" #The text has been translated
        # filter_condition = elem[0]['collection'] == "Gutenberg" #The text belongs to the collection'Gutemberg'
                
        # if filter_condition:
            # print("The text", "'" + elem[0]['title'] + "'", 'in file', file, 'met the conditions.')

''' SAVING RESULTS'''
#We create a dataframe and assign every list to a new column
df = pd.DataFrame({ 'File': all_files,
                    'Title': titles,
                    'Author': authors,
                    'Date': dates,
                    'Century': centuries,
                    'Genre': genres,
                    'ID': ids,
                    'Translation': translations,
                    'Collection': collections,
                    'N_Tokens': [len(text) for text in all_tokens],
                    'N_Types': [len(set(text)) for text in all_types]})

#We save the dataframe into a CSV file
df.to_csv('./corpus/metadata.csv', index=False)
