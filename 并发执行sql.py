from concurrent.futures import ThreadPoolExecutor, as_completed

import pymysql
import sys

domestic_wifimodel_IP = ''
domestic_wifimodel_port = 3913
domestic_user = ''
domestic_password = ''
domestic_db = ''

PROCE_NUM = 10
args = sys.argv

t_wifimodel_sql = ["drop table if exists test.t_user_home_new_{0};", "create table test.t_user_home_new_{0} like t_user_home_new_{0};",
                 "insert into test.t_user_home_new_{0} select t1.* from t_user_home_new_{0} t1 JOIN test.tmp_out_watch t2 ON  t1.watch_id =t2.watch_id_utf8;"]


def exec_sql(n, sql):
    try:
        the_connection = pymysql.connect(host=domestic_wifimodel_IP, user=domestic_user, password=domestic_password,
                                         database=domestic_db,
                                         port=domestic_wifimodel_port)
        cursor = the_connection.cursor(pymysql.cursors.DictCursor)
        for sql_row in sql:
            cursor.execute(sql_row.format(n))
        the_connection.commit()
        print("{0} {1} complete".format(str(sql).format(n), n))
        cursor.close()
        the_connection.close()
        return True
    except Exception as e:
        print("{0} {1} failed".format(str(sql).format(n), n))
        cursor.close()
        the_connection.close()
        return False


if __name__ == '__main__':
    action = sys.argv[1]
    if action == 't_wifimodel':
        obj_list = []
        t = ThreadPoolExecutor(PROCE_NUM)
        for i in range(256):
            try:
                obj = t.submit(exec_sql, i, t_wifimodel_sql)
                obj_list.append(obj)
            except Exception as e:
                print(e)
    for future in as_completed(obj_list):
        if not future.result():
            exit(1)
