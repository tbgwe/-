import time
from  multiprocessing import *
from socket import *
from DB import DB

class Coller:
    def __init__(self):
        self.coller=DB()

    def login_verification(self, bata,conn):
        db,cur=self.coller.create_connect_cursor()
        sql='select user,password from user_info where user=%s;'
        cur.execute(sql,[bata[1]])
        query_info= cur.fetchone()
        if not query_info:
            conn.send('该用户不存在'.encode())
        else:
            if query_info[1]!=bata[2]:
                conn.send('用户密码错误'.encode())
            else:
                conn.send('验证通过'.encode())
        cur.close()
        db.close()

    def register_verification(self, bata, conn):
        db,cur=self.coller.create_connect_cursor()
        sql1= 'select user from user_info where user=%s;'
        sql2='insert into user_info (user,password,email,phone) values (%s,%s,%s,%s);'
        cur.execute(sql1, [bata[1]])
        query_info = cur.fetchone()
        if  query_info:
            conn.send('该账号已注册'.encode())
        else:
            try:
                cur.execute(sql2, [bata[1],bata[2],bata[3],bata[4]])
            except Exception as e:
                db.rollback()
                print(f"数据库错误: {e}")  # 打印具体错误信息
                conn.send('系统出错'.encode())
            else:
                db.commit()
                conn.send('已完成注册'.encode())
        cur.close()
        db.close()

    def query_word(self,bata,conn):
        db,cur=self.coller.create_connect_cursor()
        sql1= 'select word,jsp from words where word=%s;'
        sql2='insert into history_query_record (words,jsp,user_name) values (%s,%s,%s);'
        cur.execute(sql1, [bata[1]])
        query_info = cur.fetchone()
        if not query_info:
            conn.send('单词不存在'.encode())
        else:
            conn.send(query_info[1].encode())
            try:
                cur.execute(sql2,[query_info[0],query_info[1],bata[2]])
            except Exception as e:
                db.rollback()
                print(f"数据库错误: {e}")  # 打印具体错误信息
                conn.send('系统出错'.encode())
            else:
                db.commit()
        cur.close()
        db.close()

    def query_history(self, bata, conn):
        db,cur=self.coller.create_connect_cursor()
        sql= 'select words,jsp from history_query_record where user_name=%s order by id DESC limit 10;'
        cur.execute(sql,bata[1])
        for i in cur.fetchall():
            record=i[0]+':   '+i[1]
            conn.send(record.encode())
            time.sleep(0.1)
        conn.send('查询完毕'.encode())
        cur.close()
        db.close()

class Service:
    def __init__(self,addr,port):
        self.addr=addr
        self.port=port
        self.sock=socket()
        self.temple=(self.addr, self.port)
        self.collers=Coller()
    def perpare_listen(self):
        self.sock.bind(self.temple)
        self.sock.listen(5)
    def start(self):
        self.perpare_listen()
        self.recv_process()

    def recv_process(self):
        while True:
            conn,data=self.sock.accept()
            process=Process(target=self.recv_message,args=(conn,))
            process.start()
    def recv_message(self,conn):
        while True:
            data = conn.recv(1024).decode()
            if data=='':
                conn.close()
                break
            bata = data.split('\n')
            if bata[0] == '登录':
                self.collers.login_verification(bata,conn)
            if bata[0] == '注册':
                self.collers.register_verification(bata,conn)
            if bata[0] == '查询单词':
                self.collers.query_word(bata,conn)
            if bata[0] == '历史记录':
                self.collers.query_history(bata,conn)
            if bata[0] == '请求连接':
                conn.send('连接成功'.encode())

if __name__ == '__main__':
    s=Service('0.0.0.0',8090)
    s.start()


