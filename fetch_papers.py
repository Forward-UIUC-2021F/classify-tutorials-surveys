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
