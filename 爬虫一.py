from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree

#这里的路径是复制下来的表格标签，改成自己的就行
with open('D:\BaiduYunDownload\YZ Meng\work\你的综述\papapa.txt') as read_file:
	ss = read_file.read()

html1 = etree.HTML(ss)
table1 = html1.xpath('//table')
table2 = etree.tostring(table1[0], encoding='utf-8').decode()
df = pd.read_html(table2, encoding='utf-8', header=0)[0]
results = list(df.T.to_dict().values())
df.to_csv('D:\BaiduYunDownload\YZ Meng\python爬虫\std.csv',index =False) #自己的路径
