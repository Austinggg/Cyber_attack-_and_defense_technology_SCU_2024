import requests                          #用于请求网页
from bs4 import BeautifulSoup            #用于处理获取的到的网页源码数据
from urllib.parse import urlparse        #用于处理url


def baidu_search():
    """
    通过百度搜索获取指定域名下的子域名
    :param domain: 要收集子域名的目标域名
    :param pages: 要爬取的页数
    :return: 收集到的子域名列表
    """
    Subdomain = []  # 存储子域名的列表
  
    # 定义请求头，随机选择 User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56', 
        'Accept': '*/*',
        'Referer': 'https://www.baidu.com',  # 使用百度主页作为 Referer
    }

    # 发送 HTTP GET 请求
    url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=site%3Abaidu.com&fenlei=256&rsv_pq=0xa0dc664401788f85&rsv_t=e2e9WG9v%2FbpX5npDHnx%2BL32OS6hh3y9hndv%2F%2FE8xzsPCgIHQtqsYkf%2BVoDZN&rqlang=en&rsv_enter=1&rsv_dl=tb&rsv_sug3=11&rsv_sug1=5&rsv_sug7=100&rsv_sug2=0&rsv_btype=t&prefixsug=site%253Aqq.com&rsp=7&inputT=4092&rsv_sug4=4093"
    resp = requests.get(url, headers=headers)

    soup = BeautifulSoup(resp.content,'html.parser')    #创建一个BeautifulSoup对象，第一个参数是网页源码，第二个参数是Beautiful Soup 使用的 HTML 解析器，
    job_bt = soup.find_all('h2')                        #find_all()查找源码中所有<h2>标签的内容
    for i in job_bt:
        link = i.a.get('href')                          #循环获取‘href’的内容
        #urlparse是一个解析url的工具，scheme获取url的协议名，netloc获取url的网络位置
        domain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)
        if domain in Subdomain:              #如果解析后的domain存在于Subdomain中则跳过，否则将domain存入子域名表中
            pass
        else:
            Subdomain.append(domain)
            print(domain) 

baidu_search()      
        
        
    