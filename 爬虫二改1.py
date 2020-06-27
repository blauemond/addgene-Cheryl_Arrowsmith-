import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
import numpy as np
import cryptography
import certifi
import OpenSSL
import time


#打开原始文件，并且抽取ID那一列
with open('D:/BaiduYunDownload/YZ Meng/python爬虫/std_4.csv','r',encoding='UTF-8') as f1:
	reader1 = csv.DictReader(f1)
	column1 = [row['ID'] for row in reader1]

#使用ID（共845个）构成845个URL，根据URL逐个爬取网页
listr = []
for i in column1:
    listr.append('https://www.addgene.org/' + i + '/')

#准备构造新列
gene_name = []
species = []
insert_size = []
mutation = []
entrez_gene = []
tag_or_fusion_protein = []

ti = 1

#逐个爬取网页
for url in listr:
    startsm = time.time()

    r = requests.get(url)
    t = r.text
    html = etree.HTML(t)

#定位网页某些标签，从而获取每个基因的相关信息
    z1 = html.xpath("//div[@id='detail-sections']/div[3]/section[1]/ul[@class='list-unstyled']/li/div[contains(text(),'Gene')]/../text()")
    if z1 == []:
        gn = 'null'
    else:
        gn = z1[1].strip()
    gene_name.append(gn)

    z2 = html.xpath("//div[@id='detail-sections']/div[3]/section[1]/ul[@class='list-unstyled']/li/div[contains(text(),'Species')]/../text()")
    if z2 == []:
        spc = 'null'
    else:
        spc = z2[1].strip()
    species.append(spc)

    z3 = html.xpath("//div[@id='detail-sections']/div[3]/section[1]/ul[@class='list-unstyled']/li/div[contains(text(),'Insert Size')]/../text()")
    if z3 == []:
        insz = 'null'
    else:
        insz = z3[1].strip()
    insert_size.append(insz)

    z4 = html.xpath("//div[@id='detail-sections']/div[3]/section[1]/ul[@class='list-unstyled']/li/div[contains(text(),'Mutation')]/../text()")
    if z4 == []:
        mut = 'null'
    else:
        mut = z4[1].strip()
    mutation.append(mut)

    z5_1 = html.xpath("//div[@id='detail-sections']/div[3]/section[1]/ul[@class='list-unstyled']/li/div[contains(text(),'Entrez Gene')]/../a/span/text()")
    z5_2 = html.xpath("//div[@id='detail-sections']/div[3]/section[1]/ul[@class='list-unstyled']/li/div[contains(text(),'Entrez Gene')]/../text()")
    if z5_1 == [] or z5_2 == []:
        etz = 'null'
    else:
        if len(z5_2) < 4:
            etz = z5_1[0].strip()
        else:
            etz = z5_1[0].strip() + z5_2[2].strip() + z5_2[3].strip()
    entrez_gene.append(etz)

    z6 =  html.xpath("//div[@id='detail-sections']/div[3]/section[1]/ul[@class='list-unstyled']/li/span[contains(text(),'Tag')]/../ul/li/text()")
    if z6 == []:
        fp = 'null'
    else:
        fp = z6[0].strip()
    tag_or_fusion_protein.append(fp)

    endsm = time.time()
    tim = endsm - startsm
    print('运行至第',ti,'次,用时',tim)
    ti = ti + 1




#将这些信息构成新列，填充进一个新表格
book = pd.read_csv('D:/BaiduYunDownload/YZ Meng/python爬虫/std_4.csv')
book['Gene/Insert name'] = gene_name
book['Species'] = species
book['Insert Size (bp)'] = insert_size
book['Mutation'] = mutation
book['Entrez Gene'] = entrez_gene
book['Tag / Fusion Protein'] = tag_or_fusion_protein

book.to_csv('D:/BaiduYunDownload/YZ Meng/python爬虫/addgene_py_4.csv', mode = 'a', index =False)




"""
下面为随便某个基因的gene name这一项的例子
ss = list[]
r1 = requests.get(url)
t1 = r1.text
html1 = etree.HTML(t1)
z = html1.xpath("//div[@id='detail-sections']/div[3]/section[1]/ul[@class='list-unstyled']/li[1]/text()")
gn = z[1].strip()
gene_name.append(name)
"""
