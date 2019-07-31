import requests
from lxml import etree
import pymysql

url = 'http://data.10jqka.com.cn/funds/ddzz/#refCountId=db_50741cd6_397,db_509381c1_860'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1;WOW64; rv:6.0) '
                  'Gecko/20100101 Firefox/6.0',
}

html = requests.get(url,headers=headers).text
parse_html = etree.HTML(html)

num_list = parse_html.xpath('//tbody/tr/td[2]/a/text()')
name_list = parse_html.xpath('//tbody/tr/td[3]/a/text()')
stacks = []
count = 0
for i in range(len(num_list)):
    if count==20:
        break
    demo = [name_list[i],num_list[i],]
    if demo not in stacks:
        count+=1
        stacks.append(demo)
    else:
        continue
print(stacks)
print(len(stacks))


#  [['300785', 'N值得买'], ['002105', '信隆健康'], ['002453', '华软科技'], ['300167', '迪威迅'], ['600078', '澄星股份'], ['002473', '圣莱达'], ['002225', '濮耐股份'], ['000586', '汇源通信'], ['002124', '天邦股份'], ['300527', '中国应急'], ['603189', '网达软件'], ['300378', '鼎捷软件'], ['300417', '南华仪器'], ['300632', '光莆股份'], ['300424', '航新科技'], ['002915', '中欣氟材'], ['300769', '德方纳米'], ['603068', '博通集成'], ['002312', '三泰控股'], ['300253', '卫宁健康']]
db = pymysql.connect('localhost','root','123456','SSEC',charset='utf8')
cursor = db.cursor()
count = 0

for i in stacks:
    cursor.execute('select count(id) from stacks')
    res = cursor.fetchall()
    if res[0][0] == 20:
        print('数据已满')
        break
    try:

        cursor.execute('insert into stacks values(Null,%s,%s)',[i[0],i[1]])
        db.commit()
        count += 1
        print(count/20*100,'%--完成')
    except Exception as e:
        print(e)
        result = input('>>r键返回')
        if result == 'r':
            db.rollback()
            break
        else:
            continue
cursor.execute('select * from stacks')
res = cursor.fetchall()
print(res)
print(len(res))
cursor.close()
db.close()
for i in range(20):
    print(i//4+1,i%4+1,end=' ')



