import ndjson
import json
import pandas as pd
import numpy as np
import csv
import os.path
from os import path
from reader import get_result 
from django.utils.encoding import smart_str, smart_unicode
'''
Filters out the keywords to store only the papers that have a cs related keyword
'''
def store_cs_keywords():
    with open('cs_query.ndjson', 'w') as f2:
        writer = ndjson.writer(f2)
        for i in range(21, 40):
            file_name = '/scratch/scratch/pritom/mag_json/mag_papers_{}.txt'.format(i)
            print(file_name)
            if path.isfile(file_name):
                with open(file_name,'r') as f:
                    data = ndjson.load(f)
                    # feeds = ndjson.loads(f2)
                    for c in data:
                        if 'keywords' in c:
                            if 'computer science' in c['keywords'] or 'programming' in c['keywords'] or 'software' in c['keywords']:
                                writer.writerow(c)
                        elif 'fos' in c:
                            if 'computer science' in c['fos'] or 'programming' in c['fos'] or 'software' in c['fos']:
                                writer.writerow(c)
    

 '''
Adds the training features to a csv file for a given keyword.
        Parameters:
                keyword (string): A keyword to be borken down into different features. 
'''
def add_to_csv(keyword, path):
    keyword = keyword.lower()

    res1 = get_result(keyword)
    res2 = get_result('survey')
    res3 = get_result('tutorial')
    # combine the result between survey and keyword
    combined = [x for x in res1 if x in res2]
    # combine the result between tutorial and keyword.
    combined_2 = [x for x in res1 if x in res3]
    
    # combine the two results from above
    for x in combined_2:
        if x not in combined:
            combined.append(x)

        
    with open(path, 'a') as file:
        writer = csv.writer(file)
        for q in combined:
            feature = []

            # the paper's document type
            feature.append(keyword)
            # number of words of in the title
            feature.append(len(q['title'].split()))
            feature.append(q['doc_type'] == 'book')
            feature.append(q['doc_type'] == 'bookChapter')
            feature.append(q['doc_type'] == 'conference')
            feature.append(q['doc_type'] == 'dataset')
            feature.append(q['doc_type'] == 'journal')
            feature.append(q['doc_type'] == 'patent')
            feature.append(q['doc_type'] == 'repository')
            feature.append(q['doc_type'] == 'thesis')
            feature.append(q['doc_type'] == None)

            # add the year of the paper
            feature.append(q['year'])
            # add the length of the paper
            feature.append(q['page_length'])
            # add the number of citation for the paper
            feature.append(q['n_citation'])
            # add the number of authors for the paper
            feature.append(q['author_num'])
            # add the number of keywords for the paper
            feature.append(len(q['keywords']))
            # add if the keyword input is one of the keywords of the paper
            feature.append(keyword in q['keywords'])
            # add if the keyword input is in the title
            feature.append(keyword in q['title'])
            # add -1 as a default label
            feature.append(-1)
            # add the title to be later extracted as an individual feature
            feature.append(smart_str(q['title']))
            # add all the keyword to be later extracted as an individual feature
            feature.append(q['keywords'])
            writer.writerow(feature)

        
'''
Read the CSV file that contains all the keywords to train the features. 
'''     
def read_txt(path):
    data = pd.read_csv('Keywords-Springer-83K-20210405.csv')
    # conver the keyword column to an array
    keywords = np.array(data['keyword'])
    for k in keywords:
        # add all the keywords features to train
        add_to_csv(k, path)

