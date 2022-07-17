"""
    Finds surveys for a keyword from Google scholar and stores them in the keyword_pages.survey table

    (owl3 run) 100%|██████████████████████████████████████████████████| 82685/82685 [77:40:13<00:00,  3.38s/it]
"""
import sys
sys.path.append('../../')

from website_db_connect import db

from scholars_rf import get_tutorials

from tqdm import tqdm
import json

import time


if __name__ == '__main__':
    cur = db.cursor()

    cur.execute("SELECT id, name FROM keyword")
    keyword_ts = cur.fetchall()

    pbar = tqdm(total=len(keyword_ts))
    num_complete = 0

    for kw_id, keyword in keyword_ts:
        # print(type(keyword), keyword)

        res = get_tutorials(keyword, annotate_data=True)
        time.sleep(2.4) # prevents Google scholar from flagging as bot

        if len(res) > 0:
            # print(json.dumps(res, indent=4))
            # print('-' * 12)
            for t in res:
                serialized_authors = json.dumps(t['authors'])
                cur.execute(
                    """
                        INSERT INTO survey 
                        (keyword_id, url, authors, title, year) 
                        VALUES 
                        (%s, %s, %s, %s, %s)
                    """, 
                    [
                        kw_id,
                        t['url'],
                        serialized_authors,
                        t['title'],
                        t['year']
                    ]
                )

        num_complete += 1
        pbar.update(1)

        if num_complete % 100 == 0:
            db.commit()
    

    db.commit()
    pbar.close()
