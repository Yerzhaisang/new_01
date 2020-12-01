import psycopg2
import numpy as np
import os

def make_query(ls, lss, query):
    conn = None

    try:

        conn = psycopg2.connect(dbname="postgres", user="postgres", password="55695387", host="127.0.0.1")

        cur = conn.cursor()

        cur.execute("create extension aqo;")

        cur.execute("set aqo.mode = 'learn';")

        cur.execute(query)

        res = cur.fetchone()[0][0]

        dictt = {}

        dictt['whole'] = [res['Plan']['Plan Rows'], res['Plan']['Actual Rows']]
        dictt['nodes'] = []
        
        temp = res["Plan"]

        while True:
            temp = temp['Plans'][0]
            dictt['nodes'].append([temp['Plan Rows'], temp['Actual Rows']])
            if 'Plans' not in temp.keys():
                break
        L1 = 0
        L2 = 0
        for j in dictt['nodes']:
            L1 += np.abs(np.log(j[0]) - np.log(j[1]))
            L2 += (np.log(j[0]) - np.log(j[1])) * (np.log(j[0]) - np.log(j[1]))
        ls.append([1, L1, L2, res['Planning Time'], res["Execution Time"]])
        lss.append([1, res])

        cur.execute("set aqo.mode = 'controlled';")

        cur.execute("update aqo_queries set use_aqo = true, auto_tuning = false where fspace_hash = (select query_hash from aqo_query_texts where query_text=%s);", (query,))
        conn.commit()

        for i in range(199):
            print(i+1, " - iteration")
            cur.execute(query)

            dictt_with = {}

            res_with = cur.fetchone()[0][0]

            dictt_with['whole'] = [res_with['Plan']['Plan Rows'], res_with['Plan']['Actual Rows']]
            dictt_with['nodes'] = []

            temp = res_with["Plan"]
            while True:
                temp = temp['Plans'][0]
                dictt_with['nodes'].append([temp['Plan Rows'], temp['Actual Rows']])
                if 'Plans' not in temp.keys():
                    break
            L1 = 0
            L2 = 0
            for j in dictt_with['nodes']:
                L1 += np.abs(np.log(j[0]) - np.log(j[1]))
                L2 += (np.log(j[0]) - np.log(j[1])) * (np.log(j[0]) - np.log(j[1]))
            ls.append([i + 2, L1, L2, res_with['Planning Time'], res_with["Execution Time"]])
            lss.append([i + 2, res_with])
            conn.commit()
        cur.execute("drop extension aqo;")
        conn.commit()


        cur.close()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
