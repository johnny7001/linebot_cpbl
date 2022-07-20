import pymysql


db_host='sgpdb.itlab.tw'
db_user='shane'
db_password='GKbCoMubLMQ6o'
db_name='shane'
db_port=8889

class DB:
    def connect(self):
        self.conn = pymysql.connect(
                             host=db_host,
                             user=db_user,
                             password=db_password,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             port=db_port)

    def query(self, sql):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
        except pymysql.OperationalError:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            print('重新連線')
        return cursor
    def close(self):
        self.connect()
        self.conn.close()
db = DB()

sql = "select m.name, m.ig_url from cpbl_member m left join cpbl_team t on m.team_id = t.id;"
result = db.query(sql).fetchall() # result = list
print(result[0])
