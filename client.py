from socket import *
from threading import Thread
class Client:
    def __init__(self,addr,port):
        self.addr = addr
        self.port = port
        self.sock=socket()
        self.temple=(self.addr,self.port)
        self.dict={}


    def run(self):
        self.sock.connect(self.temple)
        self.sock.send('请求连接\n'.encode())
        message=self.sock.recv(1024).decode()
        if message=='连接成功':
            self.firstview()

    def firstview(self):
        while True:
            print('1.登录\n2.退出\n3.注册\n')
            option = input('请输入选项：')
            if option == '1':
                if self.login():
                    continue
            elif option == '2':
                self.sock.close()
                break
            elif option == '3':
                self.register()
            else:
                print('输入有误，请重新选择')
                continue

    def login(self):
        while True:
            while True:
                user=input('请输入登录账号：')
                if not user:
                    print('账号不能为空')
                    continue
                break
            while True:
                password=input('请输入登录密码：')
                if not user:
                    print('账号不能为空')
                    continue
                if len(password)<8 or len(password)>16:
                    print('密码位数错误')
                    continue
                break
            if self.send_login_message(user,password):
                return True
            else:
                continue

    def send_login_message(self, user, password):
        send_message='登录'+'\n'+user+'\n'+password
        self.sock.send(send_message.encode())
        recv_message=self.sock.recv(1024)
        if recv_message.decode()=='验证通过':
            print('登录成功')
            self.dict['user']=user
            self.dict['password']=password
            if self.secondview():
                return True
        else:
            print(recv_message.decode())
            return False

    def secondview(self):
        while True:
            print('1.查询单词\n2.历史记录\n3.注销')
            option = input('请输入选项：')
            if option == '1':
                self.search_words()
            elif option == '2':
                self.search_history()
            elif option == '3':
                break
            else:
                print('输入有误，请重新选择')
                continue
        return True

    def input_register_user(self):
        while True:
            user_id=input('请输入注册账号（必填）：')
            if not user_id:
                print('账号不能为空，请重新输入')
                continue
            if len(user_id)<4 or len(user_id)>20:
                print('账号长度不符，请重新输入')
                continue
            self.dict['user']=user_id
            break
    def input_register_password(self):
        while True:
            password_id=input('请输入注册密码（必填）：')
            if not password_id:
                print('密码不能为空，请重新输入')
                continue
            if len(password_id)<8 or len(password_id)>16:
                print('密码长度不符，请重新输入')
                continue
            self.dict['password']=password_id
            break
    def input_register_email(self):
        email_id = input('请输入注册邮箱（选填）：')
        self.dict['email'] = email_id
    def input_register_phone(self):
        while True:
            phone_id = input('请输入注册手机号（选填）：')
            if len(phone_id)!=11 and phone_id:
                print('手机号位数不对，请重新输入')
                continue
            self.dict['phone'] = phone_id
            break
    def register(self):
        while True:
            self.input_register_user()
            self.input_register_password()
            self.input_register_email()
            self.input_register_phone()
            message='注册'+'\n'+self.dict['user']+'\n'+self.dict['password']+'\n'+self.dict['email']+'\n'+self.dict['phone']
            if self.register_message_send(message.encode()):
                continue
            break

    def register_message_send(self, message):
        self.sock.send(message)
        recv_message=self.sock.recv(1024)
        if recv_message.decode()=='已完成注册':
            print('注册成功')
            self.secondview()
        else:
            print(recv_message.decode())
            self.dict.clear()
            return True

    def search_words(self):
        while True:
            words=input('请输入你要查询的单词：')
            if words=='##':
                print('已退出')
                break
            cx_words='查询单词'+'\n'+words+'\n'+self.dict['user']
            self.sock.send(cx_words.encode())
            recv_message=self.sock.recv(1024)
            if recv_message.decode()=='单词不存在':
                print('单词不存在，请重新查询')
                continue
            print(recv_message.decode())

    def search_history(self):
        history_record='历史记录'+'\n'+self.dict['user']
        self.sock.send(history_record.encode())
        while True:
            recv_history_record=self.sock.recv(1024).decode()
            if recv_history_record=='查询完毕':
                print('查询完毕')
                break
            print(recv_history_record)




if __name__ == '__main__':
    c=Client('127.0.0.1',8090)
    c.run()









