# To use this program, it is required to have Python and Pip installed
# To install BS, the following line will be executed in terminal: pip install beautifulsoup4
import os
from bs4 import BeautifulSoup as BS

''' The files that will be split need to be the same folder (in this case, a subfolder called 'corpus')
    Then, this script gives 2 options:
        1. Save files in separate subfolders
        2. Save all files in just one folder (in this case, the 'corpus' folder)'''

#Creation of a list of objects with the keys 'id' (the first letter of each file to split) and 'filename' (its path)
corpuslist = [{'id': 'A',
                'filename': './corpus/A-12ct.utf8.src'},
              {'id': 'B',
                'filename': './corpus/B-13ct.utf8.src'},
              {'id': 'C',
                'filename': './corpus/C-14ct.utf8.src'},
              {'id': 'D',
                'filename': './corpus/D-15ct.utf8.src'},
              {'id': 'E',
                'filename': './corpus/E-16ct.utf8.src'}]

for i in corpuslist: #A loop that iterates through every item of 'corpuslist'
    letter = i['id']
    file = i['filename']
    
    corpus = open(file, encoding='UTF-8')  #The open() function opens the file, and returns the content as a file object

    soup = BS(corpus)  #BeautifulSoup is used for web scrapping, with BS() we apply the BS model to our file
    elem = soup.findAll('text') #It returns every label that starts and ends with a given string (in this case, 'text')
    '''The purpose of the soup.findAll() step is to separate each text and save them as separate elements in a list,
    since every text is inserted between <text></text> and the metadata is included by giving attributes
    to that label (for example, 'author=' or 'date=''are both attributes of <text>)'''
    
    index = 1 #We create an index in order to name new files by the structure LETTER + NUMBER
    for j in elem: #We create a loop that iterates through every text in 'elem'
        #OPTION 1 - Save files in separate subfolders
        try:
            os.makedirs("./corpus/" + letter)
        except FileExistsError: # directory already exists
            pass
        
        newFile = open('./corpus/' + letter + '/' + letter + str(index) + '.txt', 'w')
        newFile.write(str(j))
        newFile.close()
        index += 1
            
        #OPTION 2 - Save all files in just one folder
        #newFile = open('./corpus/' + letter + str(index) + '.txt', 'w')
        #newFile.write(str(j))
        #newFile.close()
        #index += 1
