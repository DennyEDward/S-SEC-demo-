# from lxml import etree
# import requests
# import numpy as np
# import matplotlib.dates as md
# import matplotlib.pyplot as mp
# from UI import *
# def details(num,name):
#     """
#     获取并绘制数据
#     :param num:
#     :return:
#     """
#     print('start get')
#
#     """
#         获取阶段
#     """
#     url = 'http://www.aigaogao.com/tools/history.html?s={}'.format(num)
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#         'Accept-Encoding': 'gzip, deflate',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Cache-Control': 'max-age=0',
#         'Connection': 'keep-alive',
#         'Cookie': 'Hm_lvt_85261bbccca7731cac0375109980ddf5=1563243079; __utmc=90353546; __utmz=90353546.1563243079.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=90353546.1687968940.1563243079.1563243079.1563262167.2; s_histo=601678; Hm_lpvt_85261bbccca7731cac0375109980ddf5=1563264268',
#         'Host': 'www.aigaogao.com',
#         'Referer': 'http://www.aigaogao.com/tools/history.html?s={}'.format(num),
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
#
#     }
#     print('web start get')
#     html = requests.get(url,headers).text
#     print('web get over')
#     dates =[]
#     opening_prices=[]
#     hightest_prices=[]
#     lowerest_price=[]
#     closing_prices=[]
#     volumns = []
#     for i in range(90,0,-1):
#         res = etree.HTML(html).xpath('//div[@id="ctl16_contentdiv"]//tr[{}]//text()'.format(i+1))
#
#         str_list = res[0].split('/')
#         date = '-'.join([str_list[-1],str_list[0],str_list[1]])
#         dates.append(date)
#         opening_prices.append(float(res[1].replace(',','')))
#         hightest_prices.append(float(res[2].replace(',','')))
#         lowerest_price.append(float(res[3].replace(',','')))
#         closing_prices.append(float(res[4].replace(',','')))
#         volumns.append(float(res[5].replace(',','')))
#     dates = np.array(dates,dtype='M8[D]')
#     opening_prices = np.array(opening_prices)
#     hightest_prices=np.array(hightest_prices)
#     lowerest_price=np.array(lowerest_price)
#     closing_prices=np.array(closing_prices)
#     volumns = np.array(volumns)
#     print('start draw')
#     """
#         绘制阶段
#     """
#     mp.figure('S-SEC', facecolor='lightgray')  # 设定窗口标题,窗口背景色
#     mp.title(num, fontsize=18)  # 设定窗口内标题
#
#     mp.xlabel('Date', fontsize=14)  # 设定x轴标题
#     mp.ylabel('Price', fontsize=14)  # 设定y轴标题
#     mp.grid(linestyle=':')  # 设定图标网格线
#     mp.tick_params(labelsize=10)  # 设定刻度参数文字大小
#     # 设置可定定位器
#     ax = mp.gca()  # 获取当前坐标轴
#     maloc = md.WeekdayLocator(byweekday=md.MO)  # 每周一 一个主刻度
#     miloc = md.DayLocator()  # 每天一个子刻度
#     ax.xaxis.set_major_locator(maloc)
#     # 设置主刻度日期的格式
#     ax.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
#
#     ax.xaxis.set_minor_locator(miloc)
#     dates = dates.astype(md.datetime.datetime)  # 转日期格式
#
#     # 收盘走势线
#     mp.plot(dates, closing_prices, label='Closing_prices', linewidth=2, color='black', alpha=1.0)
#     # 绘制蜡烛图
#     # 调整颜色
#     rise = closing_prices >= opening_prices
#     color = [('white' if x else 'green') for x in rise]
#     ecolor = [('red' if x else 'green') for x in rise]
#     # 绘制实体
#     heights = closing_prices - opening_prices
#     mp.bar(dates, heights, 0.8, opening_prices, color=color, edgecolor=ecolor, align='center',zorder=-4)
#     # 绘制影线
#     mp.vlines(dates,lowerest_price, hightest_prices, color=ecolor, zorder=-5)
#
#     # 实现加权卷积
#     # 通过指数函数,寻求一组卷积核
#     kernel = np.exp(np.linspace(-1, 0, 5))
#     kernel = kernel[::-1]
#
#     # 绘制5日均线-加权卷积运算
#     sma53 = np.convolve(closing_prices, kernel, 'valid') / kernel.sum()
#     mp.plot(dates[4:], sma53, label='SMA-5days+', linewidth=2, color='gray', alpha=0.7, zorder=-4)
#     # print('sma5+:',sma53[-5:])
#     # 　求５日布林带
#     stds = np.zeros(sma53.size)
#     for i in range(stds.size):
#         stds[i] = closing_prices[i:i + 5].std()
#     lowers = sma53 - 2 * stds
#     mp.plot(dates[4:], lowers, label='lowers', linewidth=2, color='gray', alpha=0.2)
#     # print('lowers:',lowers[-5:])
#     uppers = sma53 + 2 * stds
#     mp.plot(dates[4:], uppers, label='uppers', linewidth=2, color='gray', alpha=0.2)
#     # print('uppers:',uppers[-5:])
#     mp.fill_between(dates[4:], uppers, lowers, uppers > lowers, color='gray', alpha=0.2, zorder=-1)
#
#     mp.legend(loc='lower right', fontsize=10, )
#     mp.gcf().autofmt_xdate()  # 自动斜化
#
#     mp.show()
#
#
# if __name__=='__main__':
#     details(600745,'实验')
#
#
#

from lxml import etree
import requests
import numpy as np
import matplotlib.dates as md
import matplotlib.pyplot as mp
from UI import *
class Details:
    def __init__(self,num,name):
        self.num = num
        self.name = name
        self.dates = []
        self.opening_prices = []
        self.hightest_prices = []
        self.lowerest_price = []
        self.closing_prices = []
        self.volumns = []
        self.plan = 0
        self.details()

    def details(self):
        """
        获取并绘制数据
        :param num:
        :return:
        """
        print('start get')

        """
            获取阶段
        """
        url = 'http://www.aigaogao.com/tools/history.html?s={}'.format(self.num)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'Hm_lvt_85261bbccca7731cac0375109980ddf5=1563243079; __utmc=90353546; __utmz=90353546.1563243079.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=90353546.1687968940.1563243079.1563243079.1563262167.2; s_histo=601678; Hm_lpvt_85261bbccca7731cac0375109980ddf5=1563264268',
            'Host': 'www.aigaogao.com',
            'Referer': 'http://www.aigaogao.com/tools/history.html?s={}'.format(self.num),
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        print('web start get')
        self.html = requests.get(url,headers).text
        print('web get over')


        self.jobs = []
        for i in range(90,0,-1):

            tt = Thread(target=self.get_msg,args=(i,))
            self.jobs.append(tt)
            tt.setDaemon(True)
            tt.start()


        # for job in self.jobs:
        #     job.join()
        #     print('回收')
        self.shows()
    def get_msg(self,i):
        """
        网页源码中获取股票日期,低开高收参数值
        :param i:
        :return:
        """
        res = etree.HTML(self.html).xpath('//div[@id="ctl16_contentdiv"]//tr[{}]//text()'.format(i+1))

        str_list = res[0].split('/')
        date = '-'.join([str_list[-1],str_list[0],str_list[1]])
        self.dates.append(date)
        self.opening_prices.append(float(res[1].replace(',','')))
        self.hightest_prices.append(float(res[2].replace(',','')))
        self.lowerest_price.append(float(res[3].replace(',','')))
        self.closing_prices.append(float(res[4].replace(',','')))
        self.volumns.append(float(res[5].replace(',','')))
        self.plan+=1
        print('进度:%.2f'%(self.plan/90*100)+'%')
        return





    def shows(self):
        """
            绘制阶段
        """
        self.dates = np.array(self.dates, dtype='M8[D]')
        self.opening_prices = np.array(self.opening_prices)
        self.hightest_prices = np.array(self.hightest_prices)
        self.lowerest_price = np.array(self.lowerest_price)
        self.closing_prices = np.array(self.closing_prices)
        self.volumns = np.array(self.volumns)
        print('start draw')
        mp.figure('S-SEC', facecolor='lightgray')  # 设定窗口标题,窗口背景色
        mp.title(self.num, fontsize=18)  # 设定窗口内标题

        mp.xlabel('Date', fontsize=14)  # 设定x轴标题
        mp.ylabel('Price', fontsize=14)  # 设定y轴标题
        mp.grid(linestyle=':')  # 设定图标网格线
        mp.tick_params(labelsize=10)  # 设定刻度参数文字大小
        # 设置可定定位器
        ax = mp.gca()  # 获取当前坐标轴
        maloc = md.WeekdayLocator(byweekday=md.MO)  # 每周一 一个主刻度
        miloc = md.DayLocator()  # 每天一个子刻度
        ax.xaxis.set_major_locator(maloc)
        # 设置主刻度日期的格式
        ax.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))

        ax.xaxis.set_minor_locator(miloc)
        dates = self.dates.astype(md.datetime.datetime)  # 转日期格式

        # 收盘走势线
        mp.plot(dates, self.closing_prices, label='Closing_prices', linewidth=2, color='black', alpha=1.0)
        # 绘制蜡烛图
        # 调整颜色
        rise = self.closing_prices >= self.opening_prices
        color = [('white' if x else 'green') for x in rise]
        ecolor = [('red' if x else 'green') for x in rise]
        # 绘制实体
        heights = self.closing_prices - self.opening_prices
        mp.bar(dates, heights, 0.8, self.opening_prices, color=color, edgecolor=ecolor, align='center',zorder=-4)
        # 绘制影线
        mp.vlines(dates,self.lowerest_price, self.hightest_prices, color=ecolor, zorder=-5)

        # 实现加权卷积
        # 通过指数函数,寻求一组卷积核
        kernel = np.exp(np.linspace(-1, 0, 5))
        kernel = kernel[::-1]

        # 绘制5日均线-加权卷积运算
        sma53 = np.convolve(self.closing_prices, kernel, 'valid') / kernel.sum()
        mp.plot(dates[4:], sma53, label='SMA-5days+', linewidth=2, color='gray', alpha=0.7, zorder=-4)
        # print('sma5+:',sma53[-5:])
        # 　求５日布林带
        stds = np.zeros(sma53.size)
        for i in range(stds.size):
            stds[i] = self.closing_prices[i:i + 5].std()
        lowers = sma53 - 2 * stds
        mp.plot(dates[4:], lowers, label='lowers', linewidth=2, color='gray', alpha=0.2)
        # print('lowers:',lowers[-5:])
        uppers = sma53 + 2 * stds
        mp.plot(dates[4:], uppers, label='uppers', linewidth=2, color='gray', alpha=0.2)
        # print('uppers:',uppers[-5:])
        mp.fill_between(dates[4:], uppers, lowers, uppers > lowers, color='gray', alpha=0.2, zorder=-1)

        mp.legend(loc='lower right', fontsize=10, )
        mp.gcf().autofmt_xdate()  # 自动斜化

        mp.show()


if __name__=='__main__':
   Details(600745,'实验')