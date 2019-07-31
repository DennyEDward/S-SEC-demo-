import tkinter as tk
from threading import Thread
from tkinter import messagebox
import pymysql as sql
import requests
import time
from lxml import etree
import json
from stack_detail import *
from gevent import monkey   # monkey 插件
from queue import Queue
import os



class SSEC:
    """
        界面可视化
    """
    def __init__(self,window):
        self.window = window
        self.table = tk.Label(self.window,bg='#2c3842')
        self.table.pack(fill='both', expand=1)
        self.image = tk.PhotoImage(file='stacks_SEG.png')
        self.db = sql.connect('localhost', 'root', '123456', 'SSEC', charset='utf8')
        self.cursor = self.db.cursor()

        self.index()
    def index(self):
        """
        主页面,默认有20枚股票
        :return:
        """
        messagebox.showwarning(title='SSEC',message='准备获取实时数据,这会占用您几秒钟,\n点击[ok]开始')
        self.label = tk.Label(self.table,bg='#2c3842')
        self.label.pack()
        self.cursor.execute('select * from stacks') # 从数据库提取股票数据(股票名称与股票编号)
        self.res = self.cursor.fetchall()
        count = -1
        stack_box = {}
        self.url = 'http://www.aigaogao.com/tools/action.aspx?act=apr'
        ths = []
        self.colors = {}
        for i in self.res:
            """
                使用多线程分别爬取20枚股票当前的涨跌状态
            """
            name = i[1]
            number = i[2]
            t = Thread(target=self.get_color,args=(name,number))
            ths.append(t)
            t.start()
        for i in ths:
            i.join()
        for i in self.res:
            """
                根据当前的涨跌状态为每一枚股票上色
            """
            count += 1
            name = i[1]
            number = i[2]
            stack_box[str(count)] = tk.Label(self.label, bg='#2c3842')
            stack_box[str(count)].grid(row=count // 4 + 1, column=count % 4 + 1, pady=6, padx=3)
            tk.Button(stack_box[str(count)], bd=1, text=name, width=10, height=2, font=('黑体', '12', 'bold'), bg=self.colors[name],
                      fg='white', command=lambda num=number, name=name: self.detail(num, name)).grid(row=1, column=1)
            tk.Button(stack_box[str(count)], bd=1, text='X', bg='#f84b4c', font=('黑体', '12', 'bold'), fg='white',
                      height=2).grid(row=1, column=2)
        self.entry = tk.Entry(self.table, width=30, font=('黑体', '12', 'bold'))
        self.entry.place(x=140, y=420)
        btn = tk.Button(self.table, width=20, text='搜索其他股票', fg='white', bg='#25a9e1')
        btn.place(x=420, y=420)

    def get_color(self,name,number):
        """
            每个线程爬取自己当前股票的颜色值
        :param name:
        :param number:
        :return:
        """
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '11',
            'Content-type': 'application/x-www-form-urlencoded',
            'Cookie': 'Hm_lvt_85261bbccca7731cac0375109980ddf5=1563243079; __utmc=90353546; __utmz=90353546.1563243079.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=90353546.1687968940.1563243079.1563243079.1563262167.2; __utmt=1; s_histo=601678; __utmb=90353546.12.10.1563262167; Hm_lpvt_85261bbccca7731cac0375109980ddf5=1563264268',
            'Host': 'www.aigaogao.com',
            'Origin': 'http://www.aigaogao.com',
            'Referer': 'http://www.aigaogao.com/tools/history.html?s={}'.format(number),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Prototype-Version': '1.4.0',
            'X-Requested-With': 'XMLHttpRequest',
        }

        data = {'s': str(number)}
        html = requests.post(self.url, headers=headers, data=data).text
        d = eval(html)
        num = float(d['data'][0]['change'])
        if num > 0:
            self.colors[name] = '#da7252'
        elif num == 0:
            self.colors[name] = '#747474'
        else:
            self.colors[name] = '#2db67a'











    def detail(self,num,name):

        """
            生成子进程,用于观察股票的走势
        :param num:
        :param name:
        :return:
        """
        monkey.patch_all()
        pid = os.fork()
        if pid<0:
            print('子进程创建失败')
        elif pid==0:
            Details(num,name)
        else:
            while True:
                time.sleep(0.1)
    def back_to_index(self):
        """
        返回首页函数
        :return:
        """
        os._exit(0)  # 结束子进程
        self.label.destroy()
        self.index()

    def views(self):

        self.label = tk.Label(self.table, bg='#2c3842',image=self.image)
        tk.Button(self.table,bg='#25a9e1',command=self.back_to_index)





if __name__=='__main__':
    window = tk.Tk(className='S-SEC')
    window.geometry('720x500')

    SSEC(window)
    window.mainloop()
















