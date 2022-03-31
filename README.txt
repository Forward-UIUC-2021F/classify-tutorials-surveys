This branch is the one used in the "Living Encyclopedia" website (as of March 31 2022)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Brandon Oh
"""

Install sklearn
Install Pandas
Install Whoosh
Install BeautifulSoup

google_scholars
    scholars_rf.py: function that would save the appropriate surveys and tutorials for a set of keywords
    save_csv.py: Main function that gets and saves the training dataset
    train_data.py:Functions that would train the random forrest classifier and test the accuracy
    
    expanded_tutorials.csv: Results that were classified as appropriate surveys and tutorials
    scholars_updated_3 copy.csv:trainning set for the random forrest classifier
mag
    mag_rf.py: Functions that would train the random forrest classifier and test the accuracy
    mag.py: stores the keywords and saves the training dataset
    reader.py:Functions that set up the text search 

    cs_query_2.ndjson: The full dataset that contains computer science keywords
    Keywords-Springer-83K-20210405.csv: dataset of keywords to train and test
    mag_data_2.csv:trainning set for the random forrest classifier