'''IMPORTANT:  This script is continuing what has been done with metadata.py and tokens_csv_periods.py
    The files that will be analyzed need to be in CSV format, stored in a folder (in this case, called 'tokens')
    and each of them will be in a subfolder indicating the period they belong to.'''

''' IMPORTING PACKAGES '''
import os
import math
import collections
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mtick
from matplotlib.ticker import PercentFormatter

'''LOADING THE DATA'''
#We define the path of the folder containing the tokens in CSV format
path_tokens = './corpus/csv_25_years/'
#We list the name of all the items contained in the folder (and exclude the hidden items)
folder = [f for f in os.listdir(path_tokens) if not f.startswith('.')]
#We sort the obtained list
folder.sort(key=lambda x: '{0:0>8}'.format(x).lower())
#We set a fontname for the plots 
font_name = "Raleway"

#We define the path for the table with the metadata information of all files of the corpus
df_metadata = pd.read_csv('./corpus/metadata.csv')
#We exclude the repeated texts that we have already selected by their ID number
df_metadata = df_metadata[~df_metadata.ID.isin(["CSG",
                                                "FN1", "FN2", "FNA",
                                                "C01", "C02", "C03", "C04", "C05", "C06", "C08",
                                                "C09", "C10", "C11", "C12", "C13", "C14", "C15",
                                                "C16", "C17", "C18", "C19", "C20", "C21",
                                                "GHIU", "LZ1", "LZ2",
                                                "AC3", "BC1",
                                                "TFB", "TFC", "TFD", "TFE", "TFF", "TFG", "TFH", "TFI",
                                                "TFJ", "TFK", "TFL", "TFM", "TFN", "TFO", "TFP", "TFQ",
                                                "M19",
                                                "LC2", "LC3",
                                                "CC2",
                                                "OA1",
                                                "TA1",
                                                "TR1"])]

''' DEFINING THE SEARCH '''

print("\n")

#We set the variable 'word' so as to be obtained by asking the user through the terminal
word = input('Enter word or label to search for: ').lower()
#We set a variable called "type_of_word"
type_of_word = input('(Answer in 1 word) Is it a wordform, lemma, or label?: ').lower()

#We add conditions to assign numbers to the 'type_of_word' input (they will be used as positions)
if type_of_word == 'wordform':
    type_of_word = 0
elif type_of_word == 'lemma':
    type_of_word = 1
elif type_of_word == 'label':
    type_of_word = 2
else:
    print('\n')
    print('Sorry, that is not a valid option.')
    
#We set a variable for dividing the corpus into bins
bin_size = int(input('Which size (in number of years) do you want the bins to be?: '))
#We create a list of periods using our bin size
bins = np.arange(1100, 1599 + bin_size, bin_size).tolist()
    
#We set a variable called "format_frequency" to decide the format of the y-axis when plotting frequencies
format_frequency = input('(Answer in 1 word) Do you want freq. to be absolute, relative or 1M?: ').lower()
format_genre = input('Do you want frequencies to be divided by genre?: ').lower()

print("\n")

''' DEFINING FUNCTIONS '''

#We define a function to create a table that groups files by bin using the bin size defined before
def df_files(df):
    if format_genre == 'no':
        #We create empty lists for storing the name of files analyzed, their date, date normalized, and genre
        files = []
        dates = []
        genres = []
        dates_normalized = []
        
        #We create a loop to iterate through each row of the metadata table
        for index, row in df.iterrows():
            #We save the name of the file, its date, and its genre to separate variables
            files.append(row['File'])
            dates.append(row['Date'])
            genres.append(row['Genre'])
            
            #We assing a period to the file depending on its date
            #We remove the origin date such that 0 = 1100
            temp = row['Date'] - 1100
            #We find out how many units of our interval we have (that is, how many bins)
            temp = temp/bin_size
            #We use math.floor() in case we have obtained a floating number
            temp = math.floor(temp)
            #We use the number we have obtained to indicate the index of th date in the list of bins
            mybin = bins[temp]
            #We add the normalized date to the empty list created before
            dates_normalized.append(mybin)
        #We create a dataframe with the empty lists that have just been filled  
        df = pd.DataFrame({'Period': dates_normalized,
                           'Files': files})
        #We group the table by the normalized date of the documents
        df = df.groupby(['Period'])['Files'].apply(','.join).reset_index()
    else:
        files = []
        dates = []
        genres = []
        dates_normalized = []
        
        for index, row in df.iterrows():
            files.append(row['File'])
            dates.append(row['Date'])
            genres.append(row['Genre'])
            
            temp = row['Date'] - 1100
            temp = temp/bin_size
            temp = math.floor(temp)
            mybin = bins[temp]
            
            dates_normalized.append(mybin)
            
        df = pd.DataFrame({'Period': dates_normalized,
                           'Files': files,
                           'Genre': genres})
        df = df.groupby(['Period', 'Genre'])['Files'].apply(','.join).reset_index()
    
    return df

#We define a function to create a df with the frequencies of the given word in each bin
def df_frequencies(df, all_tokens):
    #We create empty lists   
    periods = df['Period']
    occurrences = []
    size_corpora = []
    rel_freq = []
    per_million_tokens = []
    
    if 'Genre' in df.columns:
        all_genres = df['Genre']
        genres = []
    
    #We create an index for each period and set it to 0
    index_period = 0
    
    #We iterate through every period of the list of all tokens
    for period in all_tokens:
        #OPTIONAL: We print the period that is currently being analyzed as a control measure
        print('Analyzing period "' + str(periods[index_period]) + '"...')
        
        #We create empty lists
        occurrences_period = 0
        size_corpus_period = 0
        
        if 'Genre' in df.columns:
            genres.append(all_genres[index_period])
        
        #We iterate through every text of the period
        for text in period:
            size_corpus_period += len(text)
            #We iterate through every word of the text
            for word_text in text:
                #We create a condition for if the word of the text in the right column ('Token'/'Lemma'/'Label') matches the given word
                if word_text[type_of_word] == word:
                    occurrences_period +=1      
        
        occurrences.append(occurrences_period)
        size_corpora.append(size_corpus_period)
        rel_freq.append(occurrences_period/size_corpus_period)
        per_million_tokens.append((occurrences_period/size_corpus_period)*1000000)
        
        #OPTIONAL: We print the period that has just been analyzed as a control measure    
        print('Period "' + str(periods[index_period]) + '" analyzed.')
        print('\n')
        
        #We add 1 to the counter of the periods
        index_period += 1
    
    if 'Genre' in df.columns:
        #We create a dataframe with the infomation that has been retrieved
        df_frequencies = pd.DataFrame({'Period': periods,
                                       'Genre': genres,
                                       'Ntokens': size_corpora,
                                       'Absolute_freq': occurrences,
                                       'Relative_freq': rel_freq,
                                       'Per_million_tokens': per_million_tokens})
            
        #We save the df into a CSV file in a new folder called 'contexts' and a subfolder for the given word
        try:
            os.makedirs("./tables/frequencies/")
        except FileExistsError: # directory already exists
            pass
        
        df_frequencies.to_csv(f"./tables/frequencies/{word}_by_genre.csv", index=False)
    
    else:
        #We create a dataframe with the infomation that has been retrieved
        df_frequencies = pd.DataFrame({'Period': periods,
                                        'Ntokens': size_corpora,
                                        'Absolute_freq': occurrences,
                                        'Relative_freq': rel_freq,
                                        'Per_million_tokens': per_million_tokens})
            
        #We save the df into a CSV file in a new folder called 'contexts' and a subfolder for the given word
        try:
            os.makedirs("./tables/frequencies/")
        except FileExistsError: # directory already exists
            pass
        
        df_frequencies.to_csv(f"./tables/frequencies/{word}.csv", index=False)
            
        
    #We return the list of all contexts
    return df_frequencies

#We define a function to create a lineplot with the frequencies
def plot_frequencies(df):
    if 'Genre' in df.columns:
        
        df = df.loc[df["Genre"] != "letters"]
        
        if format_frequency == 'absolute':
            y_axis = 'Absolute_freq'
            y_label = 'Absolute frequency'
            title = f"Chronological evolution of the absolute frequency of '{word}' by genre"
            name_file = f'lineplot_genre_ab_freq_{word}'
        elif format_frequency == 'relative':
            y_axis = 'Relative_freq'
            y_label == 'Relative frequency'
            title = f"Chronological evolution of the relative frequency of '{word}' by genre"
            name_file = f'lineplot_genre_rel_freq_{word}'
        elif format_frequency == '1m':
            y_axis = 'Per_million_tokens'
            y_label = 'Relative frequency (per million tokens)'
            title = f"Chronological evolution of the frequency per million of '{word}' by genre"
            name_file = f'lineplot_genre_freq_million_{word}'
        
        #We set the size of the plot
        plt.figure(figsize=(15, 8))
        
        # if word =='ser' or word=='estar' and format_frequency == '1m':
        #     plt.figure(figsize=(20, 15))
        # else:
        #     plt.figure(figsize=(25, 6))
            
        #We add colors to the datapoints depending on the genre of the document
        colors = {'law':'green', 'didactics':'darkorange', 'prose':'red',
                  'religion':'sienna', 'history':'blueviolet', 'poetry':'blue', 'medicine':'magenta'}
        #We plot results with Seaborn and use the hue parameter for dividing results by genre
        sns.lineplot(x='Period', y=y_axis, data=df, hue='Genre', palette=colors)
        #We add a legend
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=15)
        plt.legend(loc='upper left', fontsize=15)
        #We set the font size and title of the X-axis and Y-axis
        plt.xlabel('Year', font=font_name, weight="bold", fontsize=20)
        plt.xticks(np.arange(1100, 1600, bin_size), fontsize=15, font=font_name)
        plt.ylabel(y_label, fontsize=20, font=font_name, weight="bold")
        plt.yticks(fontsize=15, font=font_name)
        
        # if word == 'ser' or word == 'estar' and format_frequency == '1m':
        #     plt.yticks(np.arange(0, 45000, 2500), fontsize=15)
        # else:
        #     plt.yticks(fontsize=15)
        
        #We add a grid to the plot to facilitate the understanding of it
        # sns.set_theme()
        plt.grid(b=True, which='major', color='black', linewidth=0.075)
        plt.grid(b=True, which='minor', color='black', linewidth=0.075)
        #We create a specific subfolder for plots
        try:
            os.makedirs("./plots/lineplot/")
        except FileExistsError: # directory already exists
            pass
        #We add a title to the plot and save it into a PNG file
        # plt.title(title,fontsize=20, font=font_name, weight="bold")
        plt.savefig('./plots/lineplot/' + name_file + '.png', bbox_inches='tight')
        plt.show()
        
    else:
        #We set the Y-Axis numbers and label, as well as the title of the plot, depending on the user's input
        if format_frequency == 'absolute':
            y = df['Absolute_freq']
            y_label = 'Absolute frequency'
            title = f"Chronological evolution of the absolute frequency of '{word}'"
            name_file = f'lineplot_ab_freq_{word}'
        elif format_frequency == 'relative':
            y = df['Relative_freq']
            y_label == 'Relative frequency'
            title = f"Chronological evolution of the relative frequency of '{word}'"
            name_file = f'lineplot_rel_freq_{word}'
        elif format_frequency == '1m':
            y = df['Per_million_tokens']
            y_label = 'Relative frequency (per million tokens)'
            title = f"Chronological evolution of the frequency per million of '{word}'"
            name_file = f'lineplot_freq_million_{word}'
        
        #We configure the size of the plot
        if word == 'ser' or word == 'estar' and format_frequency == '1m':
            plt.rcParams["figure.figsize"] = (15,10)
        elif word == 'haber' or word == 'tener' and format_frequency == '1m':
            plt.rcParams["figure.figsize"] = (15,10)
        else:
            plt.rcParams["figure.figsize"] = (15,5)
        #We display the data using a line plot
        if word.lower() == "estar":
            plt.plot(df['Period'], y, linewidth=1, color='tab:orange')
        elif word.lower() == "ser":
            plt.plot(df['Period'], y, linewidth=1, color='b')
        else:
            plt.plot(df['Period'], y, linewidth=1, color='b')
        #We specify the axis labels
        plt.ylabel(y_label, fontsize=15, font=font_name, weight="bold")
        plt.xlabel('Year', fontsize=15, font=font_name, weight="bold")
        #We adjust the axis sizes and the range of the X-Axis
        plt.xticks(np.arange(1100, 1600, bin_size), fontsize=12, font=font_name)
        if word == 'ser' or word == 'estar' and format_frequency == '1m':
            plt.yticks(np.arange(1500, 30000, 1500), fontsize=12, font=font_name)
        elif word == 'haber' or word == 'tener' and format_frequency == '1m':
            plt.yticks(np.arange(2000, 18000, 2000), fontsize=12, font=font_name)
        else:
            plt.yticks(fontsize=12, font=font_name)
        #We add a grid to the plot to facilitate the understanding of it
        # sns.set_theme()
        plt.grid(b=True, which='major', color='black', linewidth=0.08)
        plt.grid(b=True, which='minor', color='black', linewidth=0.08)
        
        #We create a new folder for storing the plots
        try:
            os.makedirs("./plots/lineplot/")
        except FileExistsError: # directory already exists
            pass
        
        #We add a title to the plot and save the plot into a PNG file
        plt.title(title,fontsize=20, font=font_name, weight="bold");
        plt.savefig("./plots/lineplot/" + name_file + '.png', bbox_inches='tight')
        #We display the line plot
        plt.show()
    
    return plt

#We define a function to save the frequency of the given word by document
def df_frequencies_by_doc(df_metadata):
    #We create empty lists for storing the name of files analyzed, their date and genre, the n. of occurrences,
    #the relative frequency and the frequency per million of a given word, as well as de n. of tokens of each doc
    files = []
    dates = []
    genres = []
    occurrences = []
    rel_freq = []
    freqs_per_million = []
    size_corpora = []

    #We create a loop to iterate through each row of the metadata table
    for index, row in df_metadata.iterrows():
        #We save the name of the file, its date, and its genre to separate variables
        TXT_file = row['File']
        date = row['Date']
        genre = row['Genre']

        #We create a loop to iterate through every subfolder of the folder 'tokens', where de CSV files are
        for period in folder:
            #We define the path of each subfolder
            path_periods = path_tokens + period + '/'
            #We list the name of CSV files contained in the subfolder of each period (and exclude the hidden items)
            subfolder = [f for f in os.listdir(path_periods) if f.endswith('.csv') and not f.startswith('.')]
            #We sort the obtained list
            subfolder.sort(key=lambda x: '{0:0>8}'.format(x).lower())
            
            
            #We create anothe loop for iterating through the CSV files of each subfolder
            for CSV_file in subfolder:
                #If the file in the subfolder coincide with the name of the file of the table (changing its extension), we analyze it
                if CSV_file == TXT_file.replace(".txt", ".csv"):
                    occurrences_file = 0
                    #We take the file as a Pandas dataframe and indicate the encoding
                    df_file = pd.read_csv(path_periods + CSV_file, encoding='UTF-8')
                    #If the condition is met, we add the name to the empty list of filenames analyzed
                    files.append(CSV_file.replace(".csv", ""))
                    #We also add its date and genre to separate lists for each
                    dates.append(date)
                    genres.append(genre)
                    
                    #We define a set of conditions for either searching in the 'Token', the 'Lemma' or the 'Label' column
                    for index, row in df_file.iterrows():
                        if row[type_of_word] == word:
                            occurrences_file +=1
                    
                    #We add the list of occurrences of each period to the empty list (so as each element belongs to a different period)
                    occurrences.append(occurrences_file)
                    #We count the number of wordforms in the file
                    size_corpus = len(df_file)
                    #We calculate and add the relative frequency to the empty list
                    rel_freq.append(occurrences_file/size_corpus)
                    #We add the number of tokens of each period to the empty list
                    size_corpora.append(size_corpus)
                    #We calculate and add the relative frequency per million tokens to the empty list
                    freqs_per_million.append((occurrences_file/size_corpus)*1000000)
                

                #If the name of the file does not correspond with the name of the file in the table, we continue iterating
                else:
                    continue
                
                #OPTIONAL: The script prints the folder that has just been analized as a control measure
                print(f'File "{TXT_file}" has been analyzed.')

    #We create a dataframe with the empty lists that have just been filled
    df = pd.DataFrame({'File': files,
                       'Date': dates,
                       'Genre': genres,
                       'Occurrences': occurrences,
                       'Relative_freq': [round(num, 8) for num in rel_freq],
                       'Per_million_tokens': [round(num, 2) for num in freqs_per_million]})
    
    #We save the df into a CSV file in a new folder called 'tables_frequencies' and subfolder 'by_document'
    try:
        os.makedirs("./tables/frequencies/by_document/")
    except FileExistsError: # directory already exists
        pass
    
    df.to_csv(f"./tables/frequencies/by_document/frequency_{word}_by_doc.csv", index=False)
    
    ########## PLOTTING IN A SCATTER PLOT #########
    
    #We define a function to apply jitter to the datapoints in the scatterplot
    def rand_jitter(arr):
        stdev = .01 * (max(arr) - min(arr))
        return arr + np.random.randn(len(arr)) * stdev
    
    #We set the Y-Axis numbers and label, as well as the title of the plot, depending on the user's input
    if format_frequency == 'absolute':
        y = df['Occurrences']
        y_label = 'Absolute frequency'
        title = f"Chronological evolution of the absolute frequency of '{word}'"
        name_file = f'scatterplot_ab_freq_{word}'
    elif format_frequency == 'relative':
        y = df['Relative_freq']
        y_label == 'Relative frequency'
        title = f"Chronological evolution of the relative frequency of '{word}'"
        name_file = f'scatterplot_rel_freq_{word}'
    elif format_frequency == '1m':
        y = df['Per_million_tokens']
        y_label = 'Relative frequency (per million tokens)'
        title = f"Chronological evolution of the frequency per million of '{word}'"
        name_file = f'scatterplot_freq_million_{word}'
        
    #OPTIONAL (recommended for MacOS devices): We set the size of the plot
    plt.rcParams["figure.figsize"] = (12,5)
    fig, ax = plt.subplots()

    #We add colors to the datapoints depending on the genre of the document
    colors = {'letters':'grey', 'law':'green', 'didactics':'darkorange', 'prose':'red',
              'religion':'sienna', 'history':'blueviolet', 'poetry':'blue', 'medicine':'magenta'}

    #We plot the date of the docs as the X-Axis and the frequency per million tokens as the Y-Axis, and add genre for the point colors
    ax.scatter(rand_jitter(df['Date']), rand_jitter(y), c=df['Genre'].map(colors),
               s=5, alpha=0.7)

    #OPTIONAL: We add the name of the file to every datapoint
    # for i, txt in enumerate(files):
    #     ax.annotate(txt, (df['Date'][i], df['Per_million_tokens'][i]))

    #We add a legend for the colors of the datapoints depending on their genre
    patch1 = mpatches.Patch(color='grey', label='Letters')
    patch2 = mpatches.Patch(color='green', label='Law')
    patch3 = mpatches.Patch(color='darkorange', label='Didactics')
    patch4 = mpatches.Patch(color='red', label='Prose')
    patch5 = mpatches.Patch(color='sienna', label='Religion')
    patch6 = mpatches.Patch(color='blueviolet', label='History')
    patch7 = mpatches.Patch(color='blue', label='Poetry')
    patch8 = mpatches.Patch(color='magenta', label='Medicine')
    plt.legend(handles=[patch1, patch2, patch3, patch4, patch5,
                        patch6, patch7, patch8],
               fontsize=10, bbox_to_anchor=(1, 1), loc='upper left')
     
    #We specify the axis labels
    plt.xlabel('Year', fontsize=12, font=font_name, weight="bold")
    plt.ylabel(y_label, fontsize=12, font=font_name, weight="bold")
    #We adjust the axis sizes and configure the numbers showed in the X-Axis 
    plt.xticks(np.arange(1100, 1650, 50), fontsize=10, font=font_name)
    plt.yticks(fontsize=10, font=font_name)
    #We add a grid to the plot to facilitate the understanding of it
    plt.grid(b=True, which='major', color='black', linewidth=0.05)
    plt.grid(b=True, which='minor', color='black', linewidth=0.05)

    #We create a specific folder for the scatterplots
    try:
        os.makedirs("./plots/scatterplot/")
    except FileExistsError: # directory already exists
        pass

    #We add a title to the plot and save the plot into a PNG file
    plt.title(title,fontsize=20, font=font_name, weight="bold");
    plt.savefig('./plots/scatterplot/' + name_file + '.png', bbox_inches='tight', dpi=200)
    #We display the scatter plot
    plt.show()
    
    return df
    
#We define a version of plot_frequencies(), but for the nº of tokens of all the corpus (sampled or not)
def plot_corpus(df):
    
    df['N_Texts'] = 1
    
    dates_normalized = []
    #We create a loop to iterate through each row of the metadata table
    for index, row in df.iterrows():  
        #We remove the origin date such that 0 = 1100
        temp = row['Date'] - 1100
        #We find out how many units of our interval we have (that is, how many bins)
        temp = temp/50
        #We use math.floor() in case we have obtained a floating number
        temp = math.floor(temp)
        #We use the number we have obtained to indicate the index of th date in the list of bins
        mybin = bins[temp]
        #We add the normalized date to the empty list created before
        dates_normalized.append(mybin)

    df['Period'] = dates_normalized
    
    if format_genre == 'yes':
        df = df.groupby(['Period', 'Genre'])['N_Tokens', 'N_Types', 'N_Texts'].sum().reset_index()
        
        try:
            os.makedirs("./tables/corpus/")
        except FileExistsError: # directory already exists
            pass
    
        df.to_csv("./tables/corpus/corpus_genre_ntokens.csv", index=False)
        
        #We set the size of the plot
        plt.figure(figsize=(15, 6))
            
        #We add colors to the datapoints depending on the genre of the document
        colors = {'letters':'grey', 'law':'green', 'didactics':'darkorange', 'prose':'red',
                  'religion':'sienna', 'history':'blueviolet', 'poetry':'blue', 'medicine':'magenta'}
        
        #We plot results with Seaborn and use the hue parameter for dividing results by genre
        sns.lineplot(x='Period', y='N_Tokens', data=df, hue='Genre', palette=colors)
        
        #We add a legend
        plt.legend(bbox_to_anchor=(1, 0.5), loc='center left', fontsize=18)
        #We set the font size and title of the X-axis and Y-axis
        
        # plt.xlabel('Century', fontsize=25)
        plt.xlabel('Year', fontsize=25, font=font_name, weight="bold")
        
        # plt.xticks(np.arange(12, 17, 1), fontsize=20)
        plt.xticks(np.arange(1100, 1600, bin_size), fontsize=20, font=font_name)
        
        plt.ylabel('Size (in million tokens)', fontsize=25, font=font_name, weight="bold")
        plt.yticks(fontsize=20, font=font_name)
        
        #We add a grid to the plot to facilitate the understanding of it
        plt.grid(b=True, which='major', color='black', linewidth=0.075)
        plt.grid(b=True, which='minor', color='black', linewidth=0.075)
        
        #We create a specific subfolder for plots
        try:
            os.makedirs("./plots/lineplot/")
        except FileExistsError: # directory already exists
            pass
        #We add a title to the plot and save it into a PNG file
        plt.title(f'Pre-processed corpus token size by {bin_size}-year bins and genre',
                  fontsize=23, font=font_name, weight="bold")
        
        plt.savefig('./plots/lineplot/lineplot_corpus_genre.png', bbox_inches='tight')
        plt.show()
        
    else:
        df = df.groupby(['Period'])['N_Tokens', 'N_Types', 'N_Texts'].sum().reset_index()
        
        try:
            os.makedirs("./tables/corpus/")
        except FileExistsError: # directory already exists
            pass
    
        df.to_csv("./tables/corpus/corpus_ntokens.csv", index=False)
        
        
        x = [str(x) for x in df['Period']]
        y = df['N_Tokens']
        
        #We configure the size of the plot
        plt.rcParams["figure.figsize"] = (10,8)
        #We display the data using a line plot
        plt.bar(x, y, color='blue', ec= 'black',alpha = 0.5, width=0.8)
        #We specify the axis labels
        plt.xlabel('Year', fontsize=15, font=font_name, weight="bold")
        plt.ylabel('Size (in million tokens)', fontsize=15, font=font_name, weight="bold")
        #We adjust the axis sizes and the range of the X-Axis
        plt.xticks(fontsize=12, font=font_name)
        plt.yticks(fontsize=12, font=font_name)
        #We add a grid to the plot to facilitate the understanding of it
        # sns.set_theme()
        plt.grid(b=True, which='major', color='black', linewidth=0.05)
        plt.grid(b=True, which='minor', color='black', linewidth=0.05)
        
        #We create a new folder for the plot
        try:
            os.makedirs("./plots/histogram/")
        except FileExistsError: # directory already exists
            pass
        
        #We add a title to the plot and save the plot into a PNG file
        plt.title(f"Pre-processed corpus token size by {bin_size}-year bins",
                  fontsize=17,font=font_name, weight="bold");
        plt.savefig('./plots/histogram/ntokens_corpus.png', bbox_inches='tight', dpi=200)
       
        #We display the line plot
        plt.show()
    
    return df

#We define a function to retrieve a list with all tokens, lemmas, and labels
def list_tokens(df):
    #We create an empty list for storing the tokens
    all_tokens= []
    #We iterate through every row of the df with the files grouped by period
    for index, row in df.iterrows():
        #We assign 'period' and 'files'
        period = row['Period']
        files = row['Files'].split(',')
        if 'Genre' in df.columns:
            genre = row['Genre']
        #We create another empty list for storing the tokens of each period
        tokens_period = []
        
        #OPTIONAL: We print the period that is currently being analyzed as a control measure
        if 'Genre' in df.columns:
            print(f'Processing period "{period}" in genre "{genre}"...')
        else:
            print(f'Processing period "{period}"...')
        
        #We iterate through every file of the period
        for TXT_file in files:
            #For every file of the period in the df, we iterate through every subfolder with the tokens
            for subfolder in folder:
                #We list the name of all the CSV files contained in the subfolder (and exclude the hidden items)
                files_subfolder = [f for f in os.listdir(path_tokens + subfolder + '/') if f.endswith('.csv') and not f.startswith('.')]
                #We sort the obtained list
                files_subfolder.sort(key=lambda x: '{0:0>8}'.format(x).lower())
                #We iterate through every CSV file
                for CSV_file in files_subfolder:
                    #We set a condition for when the CSV file and the TXT file in the metadata table coincide
                    if CSV_file == TXT_file.replace(".txt", ".csv"):
                        #We open the CSV file
                        df_file = pd.read_csv(path_tokens + subfolder + '/' + CSV_file, encoding='UTF-8')
                        #We add every row of df_file to the list of tokens of the period
                        tokens_period.append(df_file.values.tolist())
        #We add the list of tokens of the period to the general list of tokens
        all_tokens.append(tokens_period)
        
        #OPTIONAL: We print the period that has just been analyzed as a control measure
        if 'Genre' in df.columns:
            print(f'Period "{period}" in genre "{genre}" proccessed.')
        else:
            print(f'Period "{period}" proccessed.')
        print('\n')
    
    #We return the list of all tokens    
    return all_tokens

#We define a function to retrieve the contexts of the given word
def return_contexts(word, df, all_tokens, window_size):
    bins = df['Period']
    
    #We create an empty list for storing all of the contexts
    all_contexts = []
    
    #We create an index for each period and set it to 0
    index_period = 0
    
    #We assign a variable to the name of the files of each period
    files = [x.split(',') for x in df['Files']]
    
    #We iterate through every period of the list of all tokens
    for period in all_tokens:
        #OPTIONAL: We print the period that is currently being analyzed as a control measure
        print('Analyzing period "' + str(bins[index_period]) + '"...')
        
        #We create empty lists with all of the contexts, printable contexts, and files with occurrences
        all_files = []
        all_contexts_period = []
        all_printable_contexts = []
        
        #We save the name of files of the current period and set another counter for the file
        files_period = files[index_period]
        index_file = 0
        
        #We iterate through every text of the period
        for text in period:
            #We set to 0 an index for the words
            index_word = 0
            #We iterate through every word of the text
            for word_text in text:
                #We create a condition for if the word of the text in the right column ('Token'/'Lemma'/'Label') matches the given word
                if word_text[type_of_word] == word:
                    if str(window_size).lower() == "r1":
                        if index_word < len(text):
                            indexes_context = [index_word, index_word+1]
                        else:
                            indexes_context = [index_word-1, index_word]
                    elif str(window_size).lower() == "l1":
                        if index_word > 0:
                            indexes_context = [index_word-1, index_word]
                        else:
                            indexes_context = [index_word, index_word+1]
                    else:
                        window_size = int(window_size)
                        #We create two variables for the starting point and ending point of the context
                        start_index = index_word - window_size
                        end_index = index_word + window_size + 1
                        
                        #We create two conditions in case the given word is at the very beginning or end of the text
                        if start_index < 0:
                            start_index = 0
                            
                        if end_index > len(text):
                            end_index = len(text)
                            
                        #We create a list for the indexes of each word of the context depending on the desirable window size
                        indexes_context = np.arange(start_index, end_index, 1).tolist()
                        
                    context = []
                    for number in indexes_context:
                        if 'nan, nan' not in str(text[number]).lower():
                            context.append(text[number])
                        else:
                            context.append(['null', 'null', 'AQ0CS0'])
                            print(text[number])
                    
                    #We also create a printable version of the context
                    printable_context = [str(word[0]) for word in context]
                    printable_context = ' '.join(printable_context)
                    printable_context = printable_context.replace(' .', '.').replace(' :', ':').replace(' ,', ',')
                    
                    #We fill the list of files, contexts, and printable contexts
                    all_files.append(files_period[index_file])
                    all_contexts.append(context)
                    all_contexts_period.append(context)
                    all_printable_contexts.append(printable_context)
                    
                #Either if the word matches or not, we add 1 to the index of the word    
                index_word +=1
            #We add 1 to the counter of the files    
            index_file += 1
        
        #We create a dataframe with the infomation that has been retrieved
        df_contexts = pd.DataFrame({'Period': bins[index_period],
                                    'File': all_files,
                                    'Context': all_contexts_period,
                                    'Printable_cont': all_printable_contexts})
        
        #We save the df into a CSV file in a new folder called 'contexts' and a subfolder for the given word
        if str(window_size).lower() == "r1":
            path = f"./tables/contexts/{word}/R1/"
            name_file = f"{bins[index_period]}_contexts_{word}_R1.csv"
        elif str(window_size).lower() == "l1":
            path = f"./tables/contexts/{word}/L1/"
            name_file = f"{bins[index_period]}_contexts_{word}_L1.csv"
        else:
            path = f"./tables/contexts/{word}/{window_size*2}-token_window/"
            name_file = f"{bins[index_period]}_contexts_{word}_{window_size*2}_window.csv"
            
        try:
            os.makedirs(path)
        except FileExistsError: # directory already exists
            pass
        
        df_contexts.to_csv(path + name_file, index=False)
        
        #OPTIONAL: We print the period that has just been analyzed as a control measure    
        print('Period "' + str(bins[index_period]) + '" analyzed.')
        print('\n')
        
        #We add 1 to the counter of the periods
        index_period += 1
    
    #We return the list of all contexts
    return all_contexts

#We define a function to retrieve the contexts of the given word
def df_contexts(all_tokens, window_size, word):   
    #We create an index for each period and set it to 0
    index_period = 0
    
    #We create empty lists with all of the contexts, printable contexts, and files with occurrences
    periods = []
    
    all_pos = []
    all_lemmas = []
    all_types = []
   
    all_occurrences = []
    size_corpora = []
    
    rel_pos = []
    rel_lemmas = []
    rel_types = []
    
    #We iterate through every period of the list of all tokens
    for period in all_tokens:
        #We merge all of the list of tokens of each document contained in 'tokens_period'
        periods.append(bins[index_period])
        
        if index_period == 1:
            index_period += 1
            
        #OPTIONAL: We print the period that is currently being analyzed as a control measure
        print('Analyzing period "' + str(bins[index_period]) + '"...')
        
        tokens_period = []
        lemmas_period = []
        pos_period = []
        
        size_corpus = 0
        occurrences = 0
        
        #We iterate through every text of the period
        for text in period:
            #We set to 0 an index for the words
            index_word = 0
            
            size_corpus += len(text)
            #We iterate through every word of the text
            for word_text in text:
                #We create a condition for if the word of the text in the right column ('Token'/'Lemma'/'Label') matches the given word
                if word_text[type_of_word] == word:
                    occurrences += 1
                                        
                    if str(window_size).lower() == "r1":
                        if index_word < len(text):
                            context = []
                            context.append(word_text)
                            context.append(text[index_word + 1])
                            for word_context in context:
                                if word_context != word_text:
                                    label = word_context[2]
                                    pos_period.append(label[0])
                                tokens_period.append(word_context[0])
                                lemmas_period.append(word_context[1])
                    elif str(window_size).lower() == "l1":
                        if index_word > 0:
                            context = []
                            context.append(text[index_word - 1])
                            context.append(word_text)
                            for word_context in context:
                                if word_context != word_text:
                                    label = word_context[2]
                                    pos_period.append(label[0])
                                tokens_period.append(word_context[0])
                                lemmas_period.append(word_context[1])
                                            
                    else:
                        window_size = int(window_size)
                        #We create two variables for the starting point and ending point of the context
                        start_index = index_word - window_size
                        end_index = index_word + window_size + 1
                        
                        #We create two conditions in case the given word is at the very beginning or end of the text
                        if start_index < 0:
                            start_index = 0
                            
                        if end_index > len(text):
                            end_index = len(text)
                            
                        #We create a list for the indexes of each word of the context depending on the desirable window size
                        indexes_context = np.arange(start_index, end_index, 1).tolist()
                        #We use the list of indexes to add the context to the general list of contexts
                        context = [text[number] for number in indexes_context]
                        for word_context in context:       
                            if word_context != word_text:
                                label = word_context[2]
                                label.split()
                                pos_period.append(label[0])
                            tokens_period.append(word_context[0])
                            lemmas_period.append(word_context[1])
                                        
                #Either if the word matches or not, we add 1 to the index of the word    
                index_word +=1
        
        
        types_period = list(set(tokens_period))
        all_types.append(types_period)
        
        set_lemmas_period = list(set(lemmas_period))
        all_lemmas.append(set_lemmas_period)

        size_corpora.append(size_corpus)

        rel_lemmas.append(len(set_lemmas_period)/occurrences)
        rel_types.append(len(types_period)/size_corpus)
        
        #OPTIONAL: We print the period that has just been analyzed as a control measure    
        print('Period "' + str(bins[index_period]) + '" analyzed.')
        print('\n')
        
        #We add 1 to the counter of the periods
        index_period += 1
    
    #We create a dataframe with the infomation that has been retrieved
    df_contexts = pd.DataFrame({'period': periods,
                                'tokens_period': size_corpora,
                                'occurrences': all_occurrences,
                                'lemmas': [len(x) for x in all_lemmas],
                                'types': [len(x) for x in all_types],
                                'rel_lemmas': rel_lemmas,
                                'rel_types': rel_types})
    
    #We save the df into a CSV file in a new folder called 'contexts' and a subfolder for the given word
    if str(window_size).lower() == "r1":
        path = "./tables/contexts/R1/"
        name_file = f"NEW_{word}_contexts_R1.csv"
    elif str(window_size).lower() == "l1":
        path = "./tables/contexts/L1/"
        name_file = f"NEW_{word}_contexts_L1.csv"
    else:
        path = f"./tables/contexts/{window_size*2}-token_window/"
        name_file = f"NEW_{word}_contexts_{window_size*2}_window.csv"
    try:
        os.makedirs(path)
    except FileExistsError: # directory already exists
        pass
    
    df_contexts.to_csv(path + name_file, index=False)  
    
    ############### PLOTTING ###################
    #Plotting collocate diversity
    df_plot = pd.DataFrame({'Period': periods,
                            'Types': rel_types})
    df_plot.set_index('Period', inplace=True)
    if str(window_size).lower() == "r1":
        title = f"Relative frequency of types in R1 position with '{word}'"
        name_file = f'{word}_lemmas_types_R1.png'
        path ="./plots/lineplot/lemmas_types/R1/"
    elif str(window_size).lower() == "l1":
        title = f"Relative frequency of types in L1 position with '{word}'"
        name_file = f'{word}_lemmas_types_L1.png'
        path ="./plots/lineplot/lemmas_types/L1/"
    else:
        title = f"Relative frequency of types occurring with '{word}' in a {window_size*2}-token window"
        name_file = f'{word}_lemmas_types_{window_size*2}_window.png'
        path = f"./plots/lineplot/lemmas_types/{window_size*2}-token_window/"
    #We set the size of the plot
    plt.figure(figsize=(12, 6))
    #We create a line plot with the dataframe
    if word.lower() == "ser":
        plt.plot(df_plot, linewidth=1, color = 'tab:orange')
    else:
        plt.plot(df_plot, linewidth=1, color = 'b')
    #We specify the axis labels
    plt.xlabel('Year', fontsize=13, font=font_name, weight="bold")
    plt.ylabel("Relative frequency", font=font_name, weight="bold", fontsize=13)
    #We adjust the axis sizes
    plt.xticks(np.arange(1100, 1600, 50), fontsize=13, font=font_name)
    plt.yticks(fontsize=13, font=font_name)
    #We add a title to the plot
    plt.title(title, font=font_name, weight="bold", fontsize=15)
    #We add a grid to the plot to facilitate the understanding of it
    # sns.set_theme()
    plt.grid(b=True, which='major', color='black', linewidth=0.075)
    plt.grid(b=True, which='minor', color='black', linewidth=0.075)
    
    #We create a specific folder for the lineplot
    try:
        os.makedirs(path)
    except FileExistsError: # directory already exists
        pass
    
    #We save the plot into a PNG file
    plt.savefig(path + name_file, bbox_inches='tight', dpi=200)
    
    
    #We return the list of all contexts
    return df_contexts

#We define a function to create a table with the freq of cooccurrences in R1 position by POS and periods
def df_pos(all_tokens, window_size, word):
    #We create an index for each period and set it to 0
    index_period = 0
    
    mydict = {}
    
    occurrences = {}
    
    #We iterate through every period of the list of all tokens
    for period in all_tokens:
        
        if index_period == 1:
            index_period += 1
        
        occurrence = 0
        
        labels = []
            
        #OPTIONAL: We print the period that is currently being analyzed as a control measure
        print('Analyzing period "' + str(bins[index_period]) + '"...')

        #We iterate through every text of the period
        for text in period:
            #We set to 0 an index for the words
            index_word = 0
            
            #We iterate through every word of the text
            for word_text in text:
                #We create a condition for if the word of the text in the right column ('Token'/'Lemma'/'Label') matches the given word
                if word_text[type_of_word] == word:
                    occurrence += 1
                    
                    if str(window_size).lower() == "r1":
                        if index_word < len(text):
                            context = []
                            context.append(word_text)
                            context.append(text[index_word + 1])
                            for word_context in context:
                                if word_context != word_text:
                                    label = word_context[2]
                                    labels.append(label[0])
                    elif str(window_size).lower() == "l1":
                        if index_word < len(text):
                            context = []
                            context.append(text[index_word - 1])
                            context.append(word_text)
                            for word_context in context:
                                if word_context != word_text:
                                    label = word_context[2]
                                    labels.append(label[0])
                    else:
                        window_size = int(window_size)
                        #We create two variables for the starting point and ending point of the context
                        start_index = index_word - window_size
                        end_index = index_word + window_size + 1
                        
                        #We create two conditions in case the given word is at the very beginning or end of the text
                        if start_index < 0:
                            start_index = 0
                            
                        if end_index > len(text):
                            end_index = len(text)
                            
                        #We create a list for the indexes of each word of the context depending on the desirable window size
                        indexes_context = np.arange(start_index, end_index, 1).tolist()
                        #We use the list of indexes to add the context to the general list of contexts
                        context = [text[number] for number in indexes_context]
                        for word_context in context:       
                            if word_context != word_text:
                                label = word_context[2]
                                labels.append(label[0])                                       
                #Either if the word matches or not, we add 1 to the index of the word    
                index_word +=1
                
        occurrences[bins[index_period]] = occurrence
        
        #We add the expanded form of each corresponding label according to the tagger Freeling
        for idx, ele in enumerate(labels):
            if ele == 'V':
                labels[idx] = 'Verbs'
            elif ele == 'A':
                labels[idx] = 'Adjectives'
            elif ele == 'D':
                labels[idx] = 'Determiners'
            elif ele == 'R':
                labels[idx] = 'Adverbs'
            elif ele == 'Q':
                labels[idx] = 'Quantifiers'
            elif ele == 'N':
                labels[idx] = 'Nouns'
            elif ele == 'T':
                labels[idx] = 'Participles'
            elif ele == 'P':
                labels[idx] = 'Pronouns'
            elif ele == 'L':
                labels[idx] = 'Clitics'
            elif ele == 'C':
                labels[idx] = 'Conjunctions'      
            elif ele == 'I':
                labels[idx] = 'Interjections'
            elif ele == 'S':
                labels[idx] = 'Prepositions'
            elif ele == 'F':
                labels[idx] = 'Punctuation'
            elif ele == 'Z':
                labels[idx] = 'Numbers' 
        
        frequency_labels = collections.Counter(labels)
        mydict[bins[index_period]] = frequency_labels
        
        #OPTIONAL: We print the period that has just been analyzed as a control measure    
        print('Period "' + str(bins[index_period]) + '" analyzed.')
        print('\n')
        
        #We add 1 to the counter of the periods

        index_period += 1
    
    df = pd.DataFrame.from_dict(mydict, orient='index')
    
    if word == "ser" or word == "estar":
        set_labels = ['Participles', 'Prepositions', 'Nouns', 'Verbs', 'Adverbs',
                      'Pronouns', 'Conjunctions', 'Determiners', 'Adjectives',
                      'Interjections', 'Numbers', 'Punctuation']
    else:
        set_labels = df.columns
        
    df = df.reset_index()
    df.rename(columns = {'index':'Period'}, inplace = True)
    
    if str(window_size).lower() == "r1":
        path = "./tables/pos/R1/"
        name_file = f"raw_{word}_pos_R1.csv"
    elif str(window_size).lower() == "l1":
        path = "./tables/pos/L1/"
        name_file = f"raw_{word}_pos_L1.csv"
    else:
        path = f"./tables/pos/{window_size*2}-token_window/"
        name_file = f"raw_{word}_pos_{window_size*2}_window.csv"
    try:
        os.makedirs(path)
    except FileExistsError: # directory already exists
        pass
    df.to_csv(path + '/raw/' + name_file, index=False)
    
    
    rel_mydict = {}
    for period in mydict: 
        elements = {}
        for key,value in dict(mydict[period]).items():
            if str(window_size).lower() == "r1" or str(window_size).lower() == "l1":
                value = value / (occurrences[period])
            else:
                value = value / (occurrences[period]*(window_size*2))
            elements[key] = value
        rel_mydict[period] = elements
    rel_df = pd.DataFrame.from_dict(rel_mydict, orient='index')
    rel_df = rel_df.reset_index()
    rel_df.rename(columns = {'index':'Period'}, inplace = True)
    
    if str(window_size).lower() == 'r1' or str(window_size).lower() == 'l1':
        rel_df.to_csv(path + f"/rel_{word}_pos_{window_size}.csv", index=False) 
    else:
        rel_df.to_csv(path + f"/rel_{word}_pos_{window_size*2}_window.csv", index=False)  
    
    ############### PLOTTING ###################
    
    #We set the 'Periods' column as the index
    rel_df.set_index('Period', inplace=True)
    if str(window_size).lower() == "r1":
        title = f"Relative frequency of POS in R1 position with '{word}'"
        name_file = f'{word}_pos_R1.png'
        path = "./plots/lineplot/pos/R1/"
    elif str(window_size).lower() == "l1":
        title = f"Relative frequency of POS in L1 position with '{word}'"
        name_file = f'{word}_pos_L1.png'
        path = "./plots/lineplot/pos/L1/"
    else:
        title = f"Relative frequency of POS occurring with '{word}' in a {window_size*2}-token window"
        name_file = f'{word}_pos_{window_size*2}_window.png'
        path = f"./plots/lineplot/pos/{window_size*2}-token_window/"
    
    #We set the size of the plot
    plt.figure(figsize=(12, 10))
    #We create a line plot with the dataframe
    plt.plot(rel_df, linewidth=1)
    #We specify the axis labels
    plt.xlabel('Year', font=font_name, weight="bold", fontsize=13)
    plt.ylabel("Relative frequency", font=font_name, weight="bold", fontsize=13)
    #We adjust the axis sizes
    plt.xticks(np.arange(1100, 1600, 50), fontsize=13, font=font_name)
    plt.yticks(fontsize=13, font=font_name)
    
    #We add a legend to the upper right corner and specify its size
    plt.legend(set_labels, loc ="center left", bbox_to_anchor=(1, 0.5), fontsize=13)
    
    #We add a title to the plot
    plt.title(title, font=font_name, weight="bold", fontsize=15)
    #We add a grid to the plot to facilitate the understanding of it
    # sns.set_theme()
    plt.grid(b=True, which='major', color='black', linewidth=0.075)
    plt.grid(b=True, which='minor', color='black', linewidth=0.075)
    
    #We create a specific folder for the lineplot
    try:
        os.makedirs(path)
    except FileExistsError: # directory already exists
        pass
    
    #We save the plot into a PNG file
    plt.savefig(path + name_file, bbox_inches='tight', dpi=200)
    #We display the line plot
    plt.show()
    
    return rel_df

def df_two_words(all_tokens, word2, df_files):
    
    bins = df_files['Period']
    
    #We create  empty lists   
    periods = []
    size_corpora = []
    
    occurrences_w1 = []
    rel_freq_w1 = []
    per_million_tokens_w1 = []
    
    occurrences_w2 = []
    rel_freq_w2 = []
    per_million_tokens_w2 = []
    
    #We create an index for each period and set it to 0
    index_period = 0
    
    
    #We iterate through every period of the list of all tokens
    for period in all_tokens:
        #OPTIONAL: We print the period that is currently being analyzed as a control measure
        print('Analyzing period "' + str(bins[index_period]) + '"...')
        
        #We create empty lists
        occurrences_period_w1 = 0
        occurrences_period_w2 = 0
        
        size_corpus_period = 0
        
        #We iterate through every text of the period
        for text in period:
            size_corpus_period += len(text)
            #We iterate through every word of the text
            for word_text in text:
                #We create a condition for if the word of the text in the right column ('Token'/'Lemma'/'Label') matches the given word
                if word_text[type_of_word] == word:
                    occurrences_period_w1 +=1
                if word_text[type_of_word] == word2:
                    occurrences_period_w2 +=1
            
        size_corpora.append(size_corpus_period)
        periods.append(bins[index_period])
        
        occurrences_w1.append(occurrences_period_w1)
        rel_freq_w1.append(occurrences_period_w1/size_corpus_period)
        per_million_tokens_w1.append((occurrences_period_w1/size_corpus_period)*1000000)
        
        occurrences_w2.append(occurrences_period_w2)
        rel_freq_w2.append(occurrences_period_w2/size_corpus_period)
        per_million_tokens_w2.append((occurrences_period_w2/size_corpus_period)*1000000)
        
        
        #OPTIONAL: We print the period that has just been analyzed as a control measure    
        print('Period "' + str(bins[index_period]) + '" analyzed.')
        print('\n')
        
        #We add 1 to the counter of the periods
        index_period += 1
        

    #We create a dataframe with the infomation that has been retrieved
    df_frequencies = pd.DataFrame({'Period': periods,
                                   'Ntokens': size_corpora,
                                   f'Absolute_freq_{word2}': occurrences_w2,
                                   f'Relative_freq_{word2}': rel_freq_w2,
                                   f'Absolute_freq_{word}': occurrences_w1,
                                   f'Relative_freq_{word}': rel_freq_w1,
                                   f'Per_million_tokens_{word}': per_million_tokens_w1,
                                   f'Per_million_tokens_{word2}': per_million_tokens_w2})
        
    #We save the df into a CSV file in a new folder called 'contexts' and a subfolder for the given word
    try:
        os.makedirs("./tables/frequencies/")
    except FileExistsError: # directory already exists
        pass
    
    df_frequencies.to_csv(f"./tables/frequencies/{word}_{word2}.csv", index=False)
            
    
    ################ PLOTTING ##############
    
    #We create a Pandas dataframe to store the collected information
    if format_frequency == 'absolute':
        df_plot = pd.DataFrame({'Period': df_frequencies['Period'],
                                word: df_frequencies[f'Absolute_freq_{word}'],
                                word2: df_frequencies[f'Absolute_freq_{word2}']})
        y_label = 'Absolute frequency'
        title = f"Chronological evolution of the absolute frequency of '{word}' and '{word2}'"
        name_file = f'lineplot_ab_freq_{word}_{word2}'
        
    elif format_frequency == 'relative':
        df_plot = pd.DataFrame({'Period': df_frequencies['Period'],
                                word: df_frequencies[f'Relative_freq_{word}'],
                                word2: df_frequencies[f'Relative_freq_{word2}']})
        y_label = 'Relative frequency'
        title = f"Chronological evolution of the relative frequency of '{word}' and '{word2}'"
        name_file = f'lineplot_rel_freq_{word}_{word2}'
        
    elif format_frequency == '1m':
        df_plot = pd.DataFrame({'Period': df_frequencies['Period'],
                                word: df_frequencies[f'Per_million_tokens_{word}'],
                                word2: df_frequencies[f'Per_million_tokens_{word2}']})
        y_label = 'Relative frequency (per million tokens)'
        title = f"Chronological evolution of the frequency per million tokens of '{word}' and '{word2}'"
        name_file = f'lineplot_freq_million_{word}_{word2}'
    
    #We set the 'Periods' column as the index
    df_plot.set_index('Period', inplace=True)
    
    #We set the size of the plot
    plt.figure(figsize=(12, 10))
    #We create a line plot with the dataframe
    plt.plot(df_plot, linewidth=1)
    #We specify the axis labels
    plt.xlabel('Year', font=font_name, weight="bold", fontsize=15)
    plt.ylabel(y_label, font=font_name, weight="bold", fontsize=15)
    #We adjust the axis sizes
    plt.xticks(np.arange(1100, 1600, 50), font=font_name, fontsize=13)
    plt.yticks(font=font_name, fontsize=13)
    #We add a legend to the upper right corner and specify its size
    plt.legend([word, word2], loc ="upper left", fontsize=15)
    #We add a title to the plot
    plt.title(title, font=font_name, weight="bold", fontsize=17)
    
    #We add a grid to the plot to facilitate the understanding of it
    # sns.set_theme()
    plt.grid(b=True, which='major', color='black', linewidth=0.075)
    plt.grid(b=True, which='minor', color='black', linewidth=0.075)
    
    #We create a specific folder for the lineplot
    try:
        os.makedirs("./plots/lineplot/")
    except FileExistsError: # directory already exists
        pass
    
    #We save the plot into a PNG file
    plt.savefig('./plots/lineplot/' + name_file + '.png', bbox_inches='tight', dpi=200)
    #We display the line plot
    plt.show()
        
    #We return the list of all contexts
    return df_frequencies

def plot_specific_pos(word2, window_size, pos):
    pos_lower = pos.lower()
    if str(window_size).lower() == "r1":
        path = "./tables/pos/R1/"
        title = f"Relative frequency of {pos_lower} occurring with '{word}/{word2}' in R1"
        name_file = f"{word}_{word2}_{pos_lower}_R1"
    elif str(window_size).lower() == "l1":
        path = "./tables/pos/L1/"
        title = f"Relative frequency of {pos_lower} occurring with '{word}/{word2}' in L1"
        name_file = f"{word}_{word2}_{pos_lower}_L1"
    else:
        path = "./tables/pos/" + str(int(window_size)*2) + "-token_window/"
        title=f"Relative frequency of {pos_lower} occurring with '{word}/{word2}' in a " + str(int(window_size)*2) + "-token window"
        name_file = f"{word}_{word2}_{pos_lower}_" + str(int(window_size)*2) + "_window"
    
    #We list the name of all the items contained in the folder (and exclude the hidden items)
    tables = [f for f in os.listdir(path) if f.startswith('rel_') and f.endswith('.csv') and not f.startswith('.')]
    
    #We sort the obtained list
    tables.sort(key=lambda x: '{0:0>8}'.format(x).lower())
    
    df_estar = pd.read_csv(path + tables[0], encoding='UTF-8')
    df_ser = pd.read_csv(path + tables[1], encoding='UTF-8')
    
    df_plot = pd.DataFrame({'Period': df_ser['Period'],
                            word: df_ser[pos],
                            word2: df_estar[pos]})
    print(df_plot)
    #We set the 'Periods' column as the index
    df_plot.set_index('Period', inplace=True)
    
    #We set the size of the plot
    plt.figure(figsize=(12, 6))
    #We create a line plot with the dataframe
    plt.plot(df_plot, linewidth=1)
    #We convert the y-axis to percentages
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    #We specify the axis labels
    plt.xlabel('Year', font=font_name, weight="bold", fontsize=13)
    plt.ylabel("Percentage", font=font_name, weight="bold", fontsize=13)
    #We adjust the axis sizes
    plt.xticks(np.arange(1100, 1600, 50), font=font_name, fontsize=13)
    plt.yticks(font=font_name, fontsize=13)
    #We add a legend to the upper right corner and specify its size
    plt.legend([word, word2], loc ="upper right", fontsize=13)
    #We add a title to the plot
    plt.title(title, font=font_name, weight="bold", fontsize=15)
    #We add a grid to the plot to facilitate the understanding of it
    # sns.set_theme()
    plt.grid(b=True, which='major', color='black', linewidth=0.075)
    plt.grid(b=True, which='minor', color='black', linewidth=0.075)
    
    #We create a specific folder for the lineplot
    if str(window_size).lower() == "r1":
        path2 = f"./plots/lineplot/pos/{word}_{word2}/{pos}/R1/"
    elif str(window_size).lower() == "l1":
        path2 = f"./plots/lineplot/pos/{word}_{word2}/{pos}/L1/"
    else:
        path2 = f"./plots/lineplot/pos/{word}_{word2}/{pos}/" + str(int(window_size)*2) + "-token_window/"
    try:
        os.makedirs(path2)
    except FileExistsError: # directory already exists
        pass
    
    #We save the plot into a PNG file
    plt.savefig(path2 + name_file + '.png', bbox_inches='tight', dpi=200)
    #We display the line plot
    plt.show()


''' RETRIEVING CONTEXTS '''
#We ask for the context window size for the given word
window_size = input('How many words do you want by each side in the context?\n(For L1 and R1 positions, enter one of those values): ')
print("\n")

################## General contexts ##################
# df_files = df_files(df_metadata)
# all_tokens = list_tokens(df_files)
# contexts = return_contexts(word, df_files, all_tokens, window_size)

################## POS/Lemma/Types table ##################
# df_files = df_files(df_metadata)
# all_tokens = list_tokens(df_files)
# contexts = df_contexts(all_tokens, window_size, word)

################## POS-specific table ##################
# df_files = df_files(df_metadata)
# all_tokens = list_tokens(df_files)
# df_pos = df_pos(all_tokens, window_size, word)

word2 = input('(Same wordtype as word 1) Enter another word or label to search for: ').lower()
print("\nAvailable POS tags:\nConjunctions\nPronouns\nPrepositions\nAdverbs\nNouns\nDeterminers\nVerbs\nParticiples\nAdjectives\nInterjections\nPunctuation\nNumbers\n")
pos = input('Which POS tag do you want to analyze?: ')
plot_specific_pos = plot_specific_pos(word2, window_size, pos)

''' PLOTTING FREQUENCIES '''
################## General/by genre ##################
# df_files = df_files(df_metadata)
# all_tokens = list_tokens(df_files)
# df_frequencies = df_frequencies(df_files, all_tokens)
# lineplot_frequencies = plot_frequencies(df_frequencies)

################## Two words ##################
# word2 = input('(Same wordtype as word 1) Enter another word or label to search for: ').lower()
# print("\n")
# df_files = df_files(df_metadata)
# all_tokens = list_tokens(df_files)
# df_two_words = df_two_words(all_tokens, word2, df_files)
    
################## By document ##################  
# df_frequencies_by_doc = table_frequencies_by_doc(df_metadata, type_of_word)
    
''' PLOTTING NUMBER OF TOKENS OF THE CORPUS '''
# df_corpus = plot_corpus(df_metadata)
