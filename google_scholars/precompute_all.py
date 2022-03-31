import sys
sys.path.append('../../')

from website_db_connect import db

from scholars_rf import get_tutorials

from tqdm import tqdm
import json


if __name__ == '__main__':
    print(get_tutorials("data mining"))
    exit()

    cur = db.cursor()

    cur.execute("SELECT id, name FROM keyword")
    keyword_ts = cur.fetchall()

    pbar = tqdm(total=len(keyword_ts))
    num_complete = 0

    for kw_id, keyword in keyword_ts:
        print(type(keyword), keyword)

        res = get_tutorials(keyword)

        if len(res) > 0:
            print(json.dumps(res, indent=4))
        # print('-' * 12)
        # for q in res:
        #     break
        #     cur.execute(
        #         "INSERT INTO question (keyword_id, content) VALUES (%s, %s)", 
        #         [kw_id, q]
        #     )

        num_complete += 1
        pbar.update(1)

        if num_complete >= 50:
            break
    

    # db.commit()
    pbar.close()
