from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import pymysql

'''用于分表很多的情况下的并发查询'''

# 查询的sql
query_sql = ''' SELECT * from t_user_app_{} WHERE package_name = 'com.sss.launcher' AND status in (3,7) AND id in (
'0c8579c627894d6a9e473494b5ba1b4256007571');'''
# 分表数量
TABLE_NUM = 200
# 并发数量
PROCE_NUM = 10
# 数据库连接信息
domestic_main_IP = '127.0.0.1'
domestic_main_port = 3306
domestic_user = 'user'
domestic_password = '123456'
domestic_main_DB = 'db1'



def data_check(n):
    the_connection = pymysql.connect(host=domestic_main_IP, user=domestic_user, password=domestic_password,
                                     database=domestic_main_DB,
                                     port=domestic_main_port)
    cursor = the_connection.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(query_sql.format(n))
        result = cursor.fetchall()
        print(result)
        threadLock.acquire()
        for arry in result:
            STR = ''
            for j in arry:
                STR = STR + str(arry[j]) + ','
            with open('result.csv', 'a') as f:
                f.write(STR + '\n')
        threadLock.release()
    except Exception as e:
        print(e)
        exit(1)

        # result_num = result[0]["count(*)"]
    cursor.close()
    the_connection.close()


if __name__ == '__main__':
    t = ThreadPoolExecutor(PROCE_NUM)
    threadLock = Lock()
    # 并发执行sql
    for i in range(TABLE_NUM):
        obj = t.submit(data_check, i)

    t.shutdown(wait=True)


########################################
# 解决pymysql返回数据为函数的问题
from pymysql import converters

conv = converters.conversions
conv[246] = float
conv[10] = str
conv[7] = str
conv[12] = str
conv[11] = str
