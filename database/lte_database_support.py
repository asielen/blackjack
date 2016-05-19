# External
import sqlite3 as lite


# Internal
from database import database
import system as syt



def lte_batch_update(sql_text, csvfile, header_len=0):
    """

    @param sql_text:
    @param csvfile:
    @param header_len;
    @return:
    """
    rows_to_process = []
    timer = syt.process_timer("Database Insert", total_tasks=len(csvfile))
    for idx, row in enumerate(csvfile):
        if idx < header_len:
            continue

        if row is None: continue

        rows_to_process.append(row)

        if idx % 10000 == 0:
            timer.log_time(len(rows_to_process))
            lte_run_batch_sql(sql_text, rows_to_process)
            rows_to_process = []

    lte_run_batch_sql(sql_text, rows_to_process)
    timer.end()


def lte_run_batch_sql(sql_text, values):
    con = lite.connect(database)

    with con:
        c = con.cursor()
        # try:
        c.executemany(sql_text, values)
        # except:
        #     print("ERROR: {}".format(sys.exc_info()[0]))

def lte_run_many_sql(sql_list):
    con = lite.connect(database)

    with con:
        c = con.cursor()
        try:
            for sql_text in sql_list:
                c.execute(sql_text)
        except Exception as e:
            print("Database Exception {}".format(e))

def lte_run_sql(sql_text, insert_list=None, one=False):
    con = lite.connect(database)

    result = None
    with con:
        c = con.cursor()
        if insert_list is not None:
            c.execute(sql_text, tuple(insert_list))
        else:
            c.execute(sql_text)
        if one:
            result = c.fetchone()
            if result is not None and isinstance(result, tuple) and len(result) == 1:  # To keep from returning (xxx,)
                result = result[0]
        else:
            result = c.fetchall()
    return result
