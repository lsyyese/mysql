import pandas as pd
import pymysql
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置valude的显示长度为100， 默认为50
pd.set_option('max_colwidth', 100)

class mysqlDB:
    def __init__(self, host, user, password, port, db="test"):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port

    def _getConnect(self):
        try:
            self.conn = pymysql.connect(host=self.host,
                                        user=self.user,
                                        passwd=self.password,
                                        port=self.port,
                                        db=self.db,
                                        )
            # cur = self.conn.cursor()
            return self.conn
        except Exception as ex:
            print("connect error")

    def ExecQuery(self, sql):
        cur = self._getConnect()
        df = pd.read_sql(sql, cur)
        return df

if __name__ == '__main__':
    domestic_main_IP = '192.168.60.128'
    domestic_main_port = 3307
    domestic_user = 'root'
    domestic_password = '123456'

    testconnect = mysqlDB(domestic_main_IP, domestic_user, domestic_password, domestic_main_port)
    result = testconnect.ExecQuery("show databases;")
    print(result.to_numpy())
