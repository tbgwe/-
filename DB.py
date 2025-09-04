import pymysql
class DB:
    def __init__(self, host='127.0.0.1', port=3306, user='root', password='123456', database='dict', charset='utf8'):
        self.dict={'host':host,'port':port,'user':user,'password':password,'database':database,'charset':charset}
    def create_connect_cursor(self):
        db=pymysql.connect(**self.dict)
        cur=db.cursor()
        return (db,cur)

if __name__ == '__main__':
    k=DB()
    sql='select word,jsp from words where word=%s;'
    k.cur.execute(sql,['abase'])
    print(k.cur.fetchone())




#alter table history_query_record add constraint tbg foreign key(user_name) references user_info(user)