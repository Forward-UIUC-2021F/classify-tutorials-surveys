import mysql.connector

import os
from dotenv import load_dotenv
load_dotenv()


if __name__ == '__main__':

    db = mysql.connector.connect(
        host="localhost",
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    cur = db.cursor()

    # Query website database for new keywords
    get_ready_kwds_sql = """
        SELECT keyword.id, name 

        FROM keyword 

        JOIN
        (
            SELECT DISTINCT(keyword.id) AS id
            FROM keyword 

            LEFT JOIN tutorial 
                ON keyword.id = keyword_id
            WHERE keyword.status='pending-info'
                AND keyword_id IS NULL
        ) AS no_tutorial_keywords
        ON keyword.id = no_tutorial_keywords.id
    """

    cur.execute(get_ready_kwds_sql)
    keywords = cur.fetchall()

    with open("new_keywords.csv", "w+") as f:

        # Write out csv header:
        header_line = "id,name\n"
        f.write(header_line)

        # Write out keywords:
        for kw_t in keywords:
            kw_id = kw_t[0]
            kw = kw_t[1].replace(',', '')

            data_line = str(kw_id) + ',' + kw + '\n'
            f.write(data_line)

