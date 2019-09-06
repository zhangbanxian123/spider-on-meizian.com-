
# coding: utf-8

# In[1]:


#coding=utf-8
import requests
from bs4 import BeautifulSoup as bs
import os
import re 
import time

ori_url = 'http://meizian.com'
all_url = 'http://meizian.com/taotu/rosi.html'
#保存地址
path = r'C:/Users/Administrator/Desktop/python_project/pachong/img/'

#http请求头
Hostreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://meizian.com/taotu/rosi.html'
               }
Picreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://meizian.com'
}
#此请求头破解盗链



# In[2]:


for j in range(1,51):
    print((all_url + '?p='+ str(j)))
    start_html = requests.get((all_url + '?p='+ str(j)),headers = Hostreferer)
    print(start_html)
    html = start_html.text
    html_tree = bs(html, "html.parser")
    # print(html_tree)
    host_infos = html_tree.find_all("div", {"class" : "image gallery-group-1"})
    # print(host_infos)
    # print(len(host_infos))

    for host_info in host_infos:
        titles = host_info.find_all("h5",{"class":"title"}) #找到
        urls = host_info.find_all('a',{'target':'_blank'})

        for title in titles:
#             print(title.string)
            title = title.string
            if (os.path.exists(path + title.replace('?',''))):
                print("\033[31m目录已存在！")
            else:
                os.makedirs(path + title.replace('?',''))
                for url in urls:
                    img_url = str(ori_url + str(url.get('href'))) #获取每个图片集的地址
                    print('正在下载：{}'.format(title))
                    img_html = requests.get(img_url,headers = Picreferer).text #获取图片集地址内容
                    img_html = bs(img_html, "html.parser") #内容规范化
                    imgs = img_html.find_all("div",{"class" : "image gallery-group-1"}) #找到页面包含每张图片地址的内容
                    print('共{}张'.format(len(imgs)))
                    for i, img in enumerate(imgs[:-4]):
                        img_lists = img.find("a") #找到包含原始图片地址的内容
    #                     print(img_lists.get('href')) #找到原始图片地址
                        pic = requests.get(img_lists.get('href'),headers = Picreferer) #获取图片
    #                     for num in range(len(imgs)):
                        file_name =path + title.replace('?','') + '/' + str(i) + '.jpg'
                        f = open(file_name , 'wb')
    #                   print('正在下载图片...',num)
                        f.write(pic.content)
                        f.close()
                print('下载完成！')
        print('\033[31m已全部下载完成！')
        start_html.close()
        time.sleep(1)

