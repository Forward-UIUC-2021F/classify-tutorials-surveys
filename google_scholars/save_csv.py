# import webbrowser
import requests
from bs4 import BeautifulSoup
import re
import time
import csv
from random import randint
# from scraper_api import ScraperAPIClient

'''
Returns a training dataset that is not labeled

    Parameters:
            keyword (string): a given keyword that would be featured
            is_survey (bool): flag that determines if the given method is looking for a survey or a tutorial
    Returns:
            all_features (list): A 2d array of all the features that are trained.
'''
def search_scholar(keyword, is_survey):
    keyword = keyword.lower()
    url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C14&q='
    url += keyword.replace(' ', '+')
    if is_survey:
        url += '+survey'
    else:
        url += '+tutorial'
    
    words = keyword.split()


    # set up requests and BeautifulSoup
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36"}
    time.sleep(randint(5, 30)) #from 5 to 30 seconds
    page = requests.get(url, headers = headers)
    
    soup = BeautifulSoup(page.content, 'html.parser')


    # first return value
    all_features = []
    # second return value
    url_list = []
    
    idx = 1 
    for item in soup.select('[data-lid]'):
        feature = []
        
        feature.append(keyword)
        # the order of the result of the search
        feature.append(idx)

        idx += 1
        # store the title
        title = item.select('h3')[0].get_text().lower()
        # store summary 
        if len(item.select('.gs_rs')) == 0:
            # check for empty summary   
            summary_ = ""
        else:
            summary_ = item.select('.gs_rs')[0].get_text()

        # get the format of the file: pdf, html, etc
        file_format = item.select('.gs_fl')[0].get_text()
        # number of citations
        citation = item.select('.gs_fl')[-1].get_text().split()
        if len(citation) > 2 and citation[2].isdigit():
            citation_num = int(citation[2])
        else:
            citation_num = -999
        expl = item.select('.gs_a')[0].get_text()
        paper = expl.split('-')

        # info section that contains the year
        info = paper[-2]
        year = -999
        if info[-5:-1].isdigit():
            year = int(info[-5:-1])
        
        # website's published year
        feature.append(year)
        # website contains pdf file
        if file_format.startswith('[PDF]') or title.startswith('[PDF]'):
            feature.append(True)
        else:
            feature.append(False)

        # website contains html format
        if file_format.startswith('[HTML]') or title.startswith('[HTML]'):
            feature.append(True)
        else:
            feature.append(False)

        is_book = item.select('span.gs_ct1')
        if len(is_book) > 0 and is_book[0].get_text() == '[BOOK]':
           feature.append(True)
        else:
            feature.append(False)

        # website is by education institute.
        flag = True
        if file_format.endswith('.edu'):
            flag = False
            feature.append(True)
        else: 
            feature.append(False)

        if file_format.endswith('.org'):
            flag = False
            feature.append(True)
        else: 
            feature.append(False)

        if file_format.endswith('.com'):
            flag = False
            feature.append(True)
        else: 
            feature.append(False)
        
        # the website ends with a different domain
        if flag and '.' in file_format:
            feature.append(True)
        else:
            feature.append(False)

        # the keyword as a whole is in the title
        if keyword in title:
            feature.append(True)
        else:
            feature.append(False)

        # all keywords in the title
        title_list = title.split()
        if all(w in title_list for w in words):
            feature.append(True)
        else:
            feature.append(False)

        # number of citations
        feature.append(citation_num)

        # length of the title
        title_length = len(title_list)

        # occurences of the words from the keyword in the title
        cnt = 0
        for w in words:
            temp = title.count(w)
            cnt += temp
            title_length -= temp 

        # number of words in the title
        feature.append(title_length)
        feature.append(cnt/ len(words))
        # occureneces of the keyword in the summary
        feature.append(summary_.count(keyword) / len(words))
        # check if ':' is in the title 
        feature.append(':' in title) 
        
        type_of_doc = ['survey', 'tutorial', 'review', 'overview']

        # if the title contains any of the type of documents
        if any(t in title for t in type_of_doc):
            feature.append(True)
        else:
            feature.append(False)
        
        # title has 'tutorial' in the title
        if type_of_doc[0] in title:
            feature.append(True)
        else:
            feature.append(False)

        # title has 'survey' in the title
        if type_of_doc[1] in title:
            feature.append(True)
        else:
            feature.append(False)

        # title has 'review' in the title
        if type_of_doc[2] in title or type_of_doc[3] in title:
            feature.append(True)
        else:
            feature.append(False)

        # average position of the keywords
        idxs = []
        for w in words:
            if w in title_list:
                idxs.append(title_list.index(w))
        
        if len(idxs) > 0:
            idx_avg = sum(idxs) / len(idxs)
            feature.append(idx_avg / len(title_list))
        else:
            feature.append(-999)


        # earliest position of the document type
        doc_idxs = []
        for d in type_of_doc:
            if d in title_list:
                doc_idxs.append(title_list.index(d))


        if len(doc_idxs) > 0:
            feature.append(min(doc_idxs) / len(title_list))
        else:
            feature.append(-999)

        feature.append(title_list)

        feature.append(summary_.split())

        # default label
        feature.append(0)
        # store the url of the search result
        url_list.append(item.select('a')[0]['href'])
        
        all_features.append(feature)
        
    return all_features, url_list


'''
Writes and saves the results of the features
    Parameters:
            keyword (string): a given keyword that would be featured

'''
def save_as_csv_(keyword):
    surveys, url1 = search_scholar(keyword, True)
    tutorials, url2 = search_scholar(keyword, False)
    with open('scholars_updated_3.csv', 'a', encoding="utf-8") as file:
        writer = csv.writer(file)
        for s in surveys:
            writer.writerow(s)
        for t in tutorials:
            writer.writerow(t)


'''
Stores all the keywords in the training dataset
    Parameters:
            keyword (string): a given keyword that would be featured
'''
def read_txt():
    f = open("keywords_training.txt", "r")
    for l in f:
        keyword = l.replace('\n', '')
        save_as_csv_(keyword)

read_txt()
print('end')


