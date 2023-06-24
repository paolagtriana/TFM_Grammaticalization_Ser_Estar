# Studying the diachrony of *ser* and *estar*
This code has been created for the Master's thesis "Grammaticalization Of Ser and Estar: A Corpus-based Study" by Paola González Triana.

The project aimed to analyze the changes in the frequency of the lemmas 'ser' and 'estar' and their combinations with other grammatical categories in R1 position during the early stages of Modern Spanish, that is, between the 12th and the 16th century. The code was used to retrieve the frequencies in CSV files and plot them through Matplotlib, and it is adapted to search for any word or label in the context, for any temporal bin and different plotting formats.

# Project order

The project was carried out executing the files in the following order:
1. *separator.py*
This script separates the texts contained in the five SRC files of the corpus and saves each one into a different TXT file.

2. *metadata.py*:
This script identifies the metadata of all files using BeautifulSoup. An option for filtering by metadata is available, and examples of this filtering option are commented.

4. *analyzer.py*
This script can be used for either retrieving the contexts of a word or plotting the frequency (general, by genre, and by doc). If plotting frequencies, these can be absolute, relative, or per million tokens, and either the full corpus or a sample of 1M of a given seed can be used as the data for the analysis, Results are saved in a CSV file and a line or scatter plot, and it is also possible to make a bar plot of the token size of the corpus (either sampled or not), and also divide the results by genre (only without sampling) and by doc (only without sampling). If retrieving the context of the occurrences of a given word, the window size of the context is specified as an input variable, and results are saved in several CSV files, one for each period.
