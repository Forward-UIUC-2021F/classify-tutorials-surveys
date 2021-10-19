def mag_get_keyword_papers(keyword, num_papers):
    print("Searching papers including keyword {}...".format(keyword))
    paper_req_attrs = 'Y,Pt,DN,CC,S,BT'
    papers_request = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?&count={}&" \
                     "expr=Composite(F.FN='{}')&attributes={}".format(str(num_papers), str(keyword).lower(), paper_req_attrs)
    response = requests.request("GET", papers_request, headers=HEADERS, data=PAYLOAD, params=QUERYSTRING)
    # expr variables wrapped in single quotes must be lower case for the MAKES API to process #
    entities = json.loads(response.text)['entities']
    for paper in entities:
        paper['keyword'] = keyword
    return entities

def delete_duplicates(papers):
    title_set = set()
    for paper in papers:
        if 'title' not in paper:
            continue
        title = paper['title'].replace(',', '').replace("'", '').replace('-', '')
        if title in title_set:
            papers.remove(paper)
        else:
            title_set.add(title)
    return papers

def write_papers_csv(papers, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['keyword', 'result_order', 'year', 'pdf', 'book', 'edu', 'org', 'com', 'other_domain',
                      'exact_keyword_title', 'all_word', 'citation#', 'title_length', 'occurences_title',
                      'occurrences_summary', 'colon', 'doc', 'survey', 'tutorial', 'review', 'position_k',
                      'position_d', 'label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for index, paper in enumerate(papers):
            obj = {}
            if 'keyword' in paper:
                obj['keyword'] = paper['keyword']
            obj['result_order'] = index
            if 'Y' in paper:
                obj['year'] = paper['Y']
            if 'S' in paper and 'Ty' in paper['S']:
                src = paper['S']['Ty']
                # Source URL type (1:HTML, 2:Text, 3:PDF, 4:DOC, 5:PPT, 6:XLS, 7:PS)
                obj['pdf'] = (src == 3)
                obj['html'] = (src == 1)
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
                obj['title_length'] = len(paper['DN'])
                obj['occurences_title'] = sum(paper['DN'].count(word) for word in paper['keyword'].split(' '))
                obj['colon'] = ':' in paper['DN']
                obj['doc'] = 'doc' in paper['DN']
                obj['survey'] = 'survey' in paper['DN']
                obj['tutorial'] = 'tutorial' in paper['DN']
                obj['review'] = 'review' in paper['DN']
            try:
                writer.writerow(obj)
            except Exception as e:
                print('Exception with paper titled: {}. Error: {}'.format(paper['DN'], str(e)))
