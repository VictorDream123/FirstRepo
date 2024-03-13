from datetime import datetime

import requests
from bs4 import BeautifulSoup

#coding:<encoding name>: #coding: utf-8
now = datetime.now()
year = now.strftime('%Y')
month = now.strftime('%m')
day = now.strftime('%d')

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

# 读取版面1所有文章的URL
response = requests.get(f"http://paper.people.com.cn/rmrb/html/{year}-{month}/{day}" '/nbs.D110000renmrb_01.htm')
html = response.text
soup = BeautifulSoup(html, "html.parser")

'''
此段代码的目的是找到网页源代码中包含版面url的对应元素
其含有多个html子标签，需要根据不同层级及其特征层层解析。
目标依次为：div,ul,li,url
 '''
all_news=soup.find ('div', attrs={"class": "news"})
for ul in all_news:
    all_ul=all_news.find("ul",attrs={"class": "news-list"})
    for li in all_ul:
        all_lis=all_ul.findAll('li')
        linkList=[]
for title in all_lis:
        tempList = title.find_all('a')
        for temp in tempList:
            link = temp["href"]
            if 'nw.D110000renmrb' in link:
                url = ("http://paper.people.com.cn/rmrb/html/"+ link)
                linkList.append(f"http://paper.people.com.cn/rmrb/html/{year}-{month}/{day}/"+link)
#保存爬取的网址
with open('urls.txt','w',encoding='UTF-8')as f:
    for url in linkList:
        f.write(url+'\n')
# 打开文件，使用 'r' 模式读取
with open('urls.txt', 'r') as f:
    # 读取每行并存储到URL列表中
    urls = [line.strip() for line in f.readlines()]

# 处理读取到的URL列表
for url in urls:
    response = requests.get(url)
    response.encoding='utf-8'

        # 如果请求成功，打印HTTP响应的状态码
    if response.status_code == 200:
            # 使用BeautifulSoup库解析HTML源代码
        soup = BeautifulSoup(response.text, 'html.parser')
            # 查找文章标题
        title = soup.h3.text+'\n'+soup.h1.text+'\n'+soup.h2.text
    print(title)
             # 查找文章内容
    pList = soup.find('div', attrs={'id': 'ozoom'}).find_all('p')
    content =""
    for p in pList:
        content += p.text + '\n'
    print(content)
# with open('爬取文章.txt', 'w', encoding='utf-8') as a:
#     f.write(title+content)
