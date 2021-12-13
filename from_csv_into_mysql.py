import csv
import pymysql
import sys
import time

'''csv文件导入mysql，按文件中的顺序依次写字段参数'''
IP = '10.0.0.1'
PORT = 3306
DB = 'test'
USER = 'root'
PW = '123456'
columns = sys.argv[1:]


def init_sql(init_row):
    for init_row_i in range(len(init_row)):
        if init_row_i == 0:
            if len(init_row) == 1:
                init_sql = "insert into TB_1117 values('{0}')".format(init_row[init_row_i])
            else:
                init_sql = "insert into TB_1117 values('{0}',".format(init_row[init_row_i])
        elif init_row_i == len(init_row) - 1 and init_row_i != 0:
            init_sql = init_sql + "'{0}')".format(init_row[init_row_i])
        else:
            init_sql = init_sql + "'{0}',".format(init_row[init_row_i])
    return init_sql


if __name__ == '__main__':
    test_Connect = pymysql.connect(host=IP, user=USER, password=PW, port=PORT,
                                    database='test')
    cursor = test_Connect.cursor()
    csv_reader = csv.reader(open("fileName.csv"))
    csv_i = 0
    for row in csv_reader:
        if csv_i == 0:
            sql = init_sql(row)
            csv_i = csv_i + 1
            continue
        if csv_i == 100:
            try:
                # cursor.execute(sql)
                print(sql)
            except Exception as e:
                print(e)
                cursor.close()
                test_Connect.close()
            time.sleep(0.05)
            for row_i in range(len(row)):
                if row_i == 0:
                    if len(row) == 1:
                        sql = "insert into TB_1117 values('{0}')".format(row[row_i])
                    else:
                        sql = "insert into TB_1117 values('{0}',".format(row[row_i])
                elif row_i == len(row) - 1 and row_i != 0:
                    sql = sql + "'{0}')".format(row[row_i])
                else:
                    sql = sql + "'{0}',".format(row[row_i])
            csv_i = 1
            continue
        if csv_i == 99:
            for row_i in range(len(row)):
                if row_i == 0:
                    if len(row) == 1:
                        sql = sql + ",('{0}');".format(row[row_i])
                    else:
                        sql = sql + ",('{0}',".format(row[row_i])
                elif row_i == len(row) - 1 and row_i != 0:
                    sql = sql + "'{0}');".format(row[row_i])
                else:
                    sql = sql + "'{0}',".format(row[row_i])
            csv_i = csv_i + 1
            continue
        else:
            for row_i in range(len(row)):
                if row_i == 0:
                    if len(row) == 1:
                        sql = sql + ",('{0}')".format(row[row_i])
                    else:
                        sql = sql + ",('{0}',".format(row[row_i])
                elif row_i == len(row) - 1 and row_i != 0:
                    sql = sql + "'{0}')".format(row[row_i])
                else:
                    sql = sql + "'{0}',".format(row[row_i])
            csv_i = csv_i + 1
            continue
     cursor.close()
     test_Connect.close()
