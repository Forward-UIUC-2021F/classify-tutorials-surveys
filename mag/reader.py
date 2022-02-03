from whoosh.index import create_in
# from whoosh.fields import *

from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NUMERIC, BOOLEAN
from whoosh.analysis import StemmingAnalyzer
from whoosh import query

import json
import ndjson

import os.path
from whoosh.index import create_in
from whoosh.index import open_dir

from whoosh.query import *
from whoosh.qparser import QueryParser

from whoosh import highlight
import os.path
from os import path

import time

"""
Reads the ndjson file and adds the document sentence by sentence of the abstracts. 
""" 
def read_data():
    schema = Schema(title=TEXT(stored=True), keywords = KEYWORD(stored = True, commas = True),doc_type=TEXT(stored=True), 
    year = NUMERIC(int, stored=True), n_citation = NUMERIC(int, stored=True), authors = KEYWORD(stored = True, commas = True), 
    author_ids = KEYWORD(stored = True, commas = True), page_length = NUMERIC(int, stored=True))

    if not os.path.exists("index"):
        os.mkdir("index")

    # create an index
    ix = create_in("index", schema)
    
    
    sizes = []
    ## add all the corpus with their submitters and abstract
    idx_ = 0
    for i in range(0, 3):
        # create writer
        writer = ix.writer()
        start = time.time()
        # file_name = 'test{}.txt'.format(i)
        file_name = '/scratch/scratch/bo7/aminer/aminer_papers_{}.txt'.format(i)
        print(file_name)
        if path.isfile(file_name):
            with open(file_name) as f:
                data = ndjson.load(f)
                ## add all the abstract to find the keyword
                for c in data:
                    idx_ += 1
                    if idx_ == 1000000:
                        break
                    if idx_ % 100000 == 0:
                        print(idx_)
                    title_ = u''
                    page_length_ = 0
                    doc_type_ = u''
                    year_ = 0
                    n_citation_ = 0
                    authors = []
                    author_ids = []
                    keywords = []
                    if 'title' in c:
                        title_ = c['title'].lower()
                    if 'doc_type' in c:
                        doc_type_ = c['doc_type'].lower()
                    if 'n_citation' in c:
                        n_citation_ = int(c['n_citation'])
                    if 'year' in c:
                        year_ = int(c['year'])
                    if 'authors' in c:
                        for i in c['authors']:
                            if 'name' in i:
                                authors.append(i[u'name'])
                            if 'id' in i:
                                author_ids.append(i[u'id'])
                    if 'page_start' in c and 'page_end' in c and type(c['page_start']) == int and type(c['page_end']) == int:
                        page_length_ = int(c['page_end']) - int(c['page_start'])
                    if 'keywords' in c:
                        keywords = c['keywords']

                    writer.add_document(title = title_, keywords = keywords, doc_type = doc_type_, year = year_, n_citation = n_citation_, 
                    authors = authors, author_ids = author_ids, page_length = page_length_)
            writer.commit() 
            end_time = time.time()
            print((len(data), end_time - start))
            sizes.append((len(data), end_time - start))
    return sizes


"""
This function takes the keyword and uses the whoosh search query to find the keyword.
After it obtains the sentences with the keyword
it checks if the keyword is used as a subject and saves the sentece if so. 
Args:
    input: The keyword to be searched

Returns:
    The sentences that contain the keyword that was the input
"""
def get_result(input):
    # open an index
    ix = open_dir("index")

    # create searcher
    searcher = ix.searcher()

    qp = QueryParser('keywords', schema=ix.schema)
    q = qp.parse('"%s"' % input)
    # allow_q = query.Term('title', 'tutorial')

    results = searcher.search(q, limit = None)
    response = [dict(hit) for hit in results]
    return response



