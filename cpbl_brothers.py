from distutils.log import error
from tempfile import tempdir
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains, ChromeOptions
from bs4 import BeautifulSoup
import requests
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

url = "https://www.pttweb.cc/bbs/CheerGirlsTW/M.1644866981.A.7E0"
# header = ''
# 設定Header與Cookie
my_headers = {'cookie': 'over18=1;'}
# 發送get 請求 到 ptt 八卦版
resp = requests.get(url, headers = my_headers)

resp.encoding='utf-8'
resp = resp.text

dragons_list = [] # 味全龍


soup = BeautifulSoup(resp, 'html.parser')
article_body = soup.find('div', {'class':'e7-main-content'})
# print(article_body)
members = article_body.find_all('span')
team_list = ['小龍女', 'Fubon Angels', '樂天女孩', 'Passion Sisters', 'Uni Girls']
for x in range(len(team_list)-1):
    dragons = article_body.text.split(team_list[x])[1].split(team_list[x+1])[0]
    listRes = list(dragons.split("\n"))
    dragons_list = [x for x in listRes if x !='']
    sql = "SELECT id FROM cpbl_team where name = '{}';".format(team_list[x])
    dragons_id = db.query(sql).fetchone()['id']
    dragons_member_list = []
    dragons_ig_list = []
    count = 0
    for d_data in dragons_list:
        if count % 2 == 0:
            if d_data == "Abu'u":
                d_data = "阿布舞"
                dragons_member_list.append(d_data)
            else:
                dragons_member_list.append(d_data)
        else:
            dragons_ig_list.append(d_data)
        count += 1

    dragons_data = dict(zip(dragons_member_list, dragons_ig_list))
    for name in dragons_data:
        # 先判定成員是否已存在於資料庫
        sql = f"select name from `cpbl_member` where name = '{name}'"
        result = db.query(sql).fetchone()
        if result == None:
            sql = "insert into `cpbl_member` (`team_id`, `name`, `ig_url`, `status`) values \
                ('{}', '{}', '{}', '{}')".format(dragons_id, name, dragons_data[f'{name}'], 1)
            db.query(sql)
            print(name, '新增成功')    
        else:
            print(name, '已存在於資料庫')
    

    
# 偶數 = 姓名, 基數 = ig_url



# for m in members:
#     content = m.text
#     if '小龍女' in content:
#         print(content.split('小龍女')[1].split('Fubon Angels')[0])
    # else:
    #     print(content.strip())
    #     if 'Fubon Angels' in content:
    #         print('-'*20)
    #         print(content.split('Fubon Angels')[1].strip())
        # if 'Fubon Angels' in content:
        #     break
    

# # def main():
# print('開始爬取')
# # 登入女神站首頁
# # PATH = "/Users/johnny7001/PythonProjects/account_cashier/chromedriver 2"
# chrome_options = ChromeOptions()

# # 不要顯示瀏覽器
# # chrome_options.add_argument('--headless')
# # 隱藏selenium的自動控制功能, 防止被偵測
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# # 設置修改selenium的特徵值, 防止被偵測
# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# # driver = webdriver.Chrome(PATH)

# user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36c'
# # chrome_options.add_argument('--user-agent=%s' % user_agent)
# driver = webdriver.Chrome('/Users/johnny7001/dns/chromedriver 2', options=chrome_options)

# # driver = webdriver.Remote(
# #     command_executor='http://10.4.17.21:4444/wd/hub',
# #     options=chrome_options
# # )

# driver.get("https://www.pttweb.cc/bbs/CheerGirlsTW")
# # driver.maximize_window()
# html_page = driver.page_source
# print(html_page)
# # if __name__ == '__main__':
# #     print('執行')
# #     main()
