import requests
import json
import csv

# API Request variables
HEADERS = {"Ocp-Apim-Subscription-Key": "0573b5f87b1f4966bc827e6b55896785"}
QUERYSTRING = {"mode": "json%0A"}
PAYLOAD = "{}"

'''
    Returns all article metadata, including label and keyword
'''


def get_fieldnames():
    return ['keyword', 'id', 'result_order', 'year', 'HTML', "Text", 'pdf', 'DOC', 'other_type', 'book', 'edu',
            'org', 'com', 'other_domain',
            'exact_keyword_title', 'all_word', 'citation#', 'title_length', 'occurences_title', 'colon',
            'doc', 'survey', 'tutorial', 'review', 'position_k', 'position_d', 'label', 'title', 'src']


def _mag_get_papers_helper(ids, paper_req_attrs, filter_func):
    # Query author's papers
    num_res = len(ids)
    match_cond = "Or(" + ",".join(["Id=" + str(id) for id in ids]) + ")"
    papers_request = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?&count={}&expr={}&attributes={}".format(
        str(num_res), match_cond, paper_req_attrs)

    response = requests.request("GET", papers_request, headers=HEADERS, data=PAYLOAD, params=QUERYSTRING)

    try:
        entities = json.loads(response.text)['entities']
        entities = [t for t in entities if filter_func(t)]
    except:
        print("API error")
        print(response.text)
        return

    # Convert and store paper information
    papers = []
    for entity in entities:
        paper = entity

        if paper is not None:
            papers.append(paper)

    return papers


def mag_get_paper(id):
    # Query author's papers
    num_res = 1
    paper_req_attrs = 'Id,DN,IA,CC,Y,AA.AuId,AA.S,AA.AfN'

    papers_request = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?&count={}&expr=Id={}&attributes={}".format(
        str(num_res), str(id), paper_req_attrs)

    response = requests.request("GET", papers_request, headers=HEADERS, data=PAYLOAD, params=QUERYSTRING)

    try:
        entity = json.loads(response.text)['entities'][0]
        return entity

    except:
        print("API error: ")
        print(response.text)


'''
Retrieves papers from MAKES API which match inputted ids
    Parameters:
            ids(List[int]): ids of papers to be fetched
    Returns:
            Paper entities(dict)
'''


def mag_get_papers(ids):
    paper_req_attrs = 'Id,DN,IA,CC,Y,AA.AuId,AA.S,AA.AfN'
    filter_func = lambda t: 'IA' in t
    return _mag_get_papers_helper(ids, paper_req_attrs, filter_func)


'''
Writes all papers and metadata to csv
For details: https://docs.microsoft.com/en-us/academic-services/knowledge-exploration-service/reference-makes-api-entity-schema?view=makes-3.0
    Parameters:
            papers(dict): papers and their metadata
            filename(str): file to write to
'''


def write_papers_csv(papers, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = get_fieldnames()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        curr_keyword = ""
        result_ind = 1
        for index, paper in enumerate(papers):
            obj = {}
            if 'keyword' in paper:
                obj['keyword'] = paper['keyword']
                if paper['keyword'] == curr_keyword:
                    obj['result_order'] = result_ind
                    result_ind += 1
                else:
                    curr_keyword = paper['keyword']
                    result_ind = 1
                    obj['result_order'] = result_ind
                    result_ind += 1
            if 'Y' in paper:
                obj['year'] = paper['Y']
            if 'Id' in paper:
                obj['id'] = paper['Id']
            got_title = False
            if 'S' in paper:
                for element in paper['S']:
                    if 'U' in element:
                        obj['src'] = element['U']
                        if element['U'].strip() != "":
                            got_title = True
                        if 'Ty' in element:
                            obj['HTML'] = (element['Ty'] == 1)
                            obj['Text'] = (element['Ty'] == 2)
                            obj['pdf'] = (element['Ty'] == 3)
                            obj['DOC'] = (element['Ty'] == 4)
                            obj['other_type'] = (element['Ty'] >= 5)
                        else:
                            obj['HTML'] = False
                            obj['Text'] = False
                            obj['pdf'] = False
                            obj['DOC'] = False
                            obj['other_type'] = False
                        break
                # src = paper['S'][['Ty']]
                # # Source URL type (1:HTML, 2:Text, 3:PDF, 4:DOC, 5:PPT, 6:XLS, 7:PS)
                # obj['pdf'] = (src == 3)
                # obj['html'] = (src == 1)
            if not got_title:
                continue
            obj['book'] = ('BT' in paper and paper['BT'] == 'b')
            obj['edu'] = ('S' in paper and 'U' in paper['S'] and 'edu' in paper['S']['U'])
            obj['org'] = ('S' in paper and 'U' in paper['S'] and 'org' in paper['S']['U'])
            obj['com'] = ('S' in paper and 'U' in paper['S'] and 'com' in paper['S']['U'])
            obj['other_domain'] = ('S' in paper and 'U' in paper['S'] and '.' in paper['S']['U'])
            obj['exact_keyword_title'] = (paper['keyword'] in paper['DN'])
            obj['all_word'] = all(w in paper['DN'].split(' ') for w in paper['keyword'].split(' '))
            if 'CC' in paper:
                obj['citation#'] = paper['CC']
            if 'DN' in paper:
                obj['title'] = paper['DN']
                obj['title_length'] = len(paper['DN'])
                obj['occurences_title'] = sum(paper['DN'].count(word) for word in paper['keyword'].split(' '))
                obj['colon'] = ':' in paper['DN']
                obj['doc'] = 'doc' in paper['DN']
                obj['survey'] = 'survey' in paper['DN']
                obj['tutorial'] = 'tutorial' in paper['DN']
                obj['review'] = 'review' in paper['DN']
                title_list = paper['DN'].split()

                if paper['keyword']:
                    # average position of the keywords
                    words = paper['keyword'].split()
                    idxs = []
                    for w in words:
                        if w in title_list:
                            idxs.append(title_list.index(w))

                    if len(idxs) > 0:
                        idx_avg = sum(idxs) / len(idxs)
                        obj['position_k'] = idx_avg / len(title_list)
                    else:
                        obj['position_k'] = 0

                # earliest position of the document type
                doc_idxs = []
                for d in ['survey', 'tutorial', 'review', 'overview']:
                    if d in title_list:
                        doc_idxs.append(title_list.index(d))

                if len(doc_idxs) > 0:
                    obj['position_d'] = (min(doc_idxs) / len(title_list))
                else:
                    obj['position_d'] = 0

            try:
                writer.writerow(obj)
            except Exception as e:
                print('Exception with paper titled: {}. Error: {}'.format(paper['DN'], str(e)))


'''
Searches keyword in MAKES API
    Parameters:
            keyword(str): keyword to search with
            num_papers(int): number of papers to retrieve
    Returns:
            Papers and their metadata (dict)
'''


def mag_get_keyword_papers(keyword, num_papers):
    print("Searching papers including keyword {}...".format(keyword))
    paper_req_attrs = 'Id,Y,Pt,DN,CC,S,BT'
    papers_request = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?&count={}&" \
                     "expr=Composite(F.FN='{}')&attributes={}".format(str(num_papers), str(keyword).lower(),
                                                                      paper_req_attrs)
    response = requests.request("GET", papers_request, headers=HEADERS, data=PAYLOAD, params=QUERYSTRING)
    # expr variables wrapped in single quotes must be lower case for the MAKES API to process #
    entities = json.loads(response.text)['entities']
    for paper in entities:
        paper['keyword'] = keyword
    return entities


'''
Deletes duplicates from papers based on title
    Parameters:
            papers(dict): papers from which duplicates are deleted
    Returns:
            papers(dict): dictionary without duplicates
            delete_count(int): number of papers deleted 
'''
def delete_duplicates(papers):
    title_set = set()
    delete_count = 0
    for paper in papers:
        if 'DN' not in paper:
            continue
        title = paper['DN'].replace(',', '').replace("'", '').replace('-', '').strip().lower()
        if title in title_set:
            delete_count += 1
            papers.remove(paper)
        else:
            title_set.add(title)
    return papers, delete_count

'''
Fetches papers based on inputted parameters
    Parameters:
            num_papers_per_keyword(int): how many papers to fetch per keyword
            num_keywords(int): num keywords in file to fetch papers for
            filename(str): file to read keywords from
    Returns:
            training_data(dict): all papers and associated metadata
'''
def fetch_papers(num_papers_per_keyword, num_keywords, filename):
    kw_file = open(filename, 'r', encoding='utf-8')
    training_data = []
    count_keywords = 0
    for line in kw_file.readlines():
        if count_keywords == num_keywords:
            break
        query_keyword = line.strip()
        try:
            papers = mag_get_keyword_papers(query_keyword, num_papers_per_keyword)
            papers, duplicates = delete_duplicates(papers)  # deletes duplicate papers
            training_data += papers
            print("Obtained {} papers - {} duplicate(s)".format(str(len(papers)), str(duplicates)))
        except:
            continue
        count_keywords += 1

    return training_data


if __name__ == '__main__':
    kPaperCount = 5
    kKeywords = 550
    training_data = fetch_papers(kPaperCount, kKeywords, 'keywords.txt')
    write_papers_csv(training_data, 'labeling_demo.csv')
