import random
import time
import requests                          # 用于发送HTTP请求获取网页内容
from bs4 import BeautifulSoup            # 用于解析和处理获取的网页源码数据
from urllib.parse import urlparse        # 用于解析URL，提取协议、网络位置等信息
from fake_useragent import UserAgent     # 用于生成随机的User-Agent，模拟浏览器访问



# 定义一个函数，用于通过百度搜索子域名
def baidu_search(domain_request, max_pages=100):
    Subdomain = []  # 定义一个空列表，用于存储收集到的子域名
    ua = UserAgent()  # 初始化 UserAgent 对象，用于随机生成 User-Agent 字符串

    page_num = 0  # 已搜索的页数初始化为 0
    found_domains = 0  # 已找到的域名数量初始化为 0

    # 定义请求头，绕过反爬机制，模拟浏览器访问
    headers = {
        'User-Agent': ua.random,  # 使用随机的 User-Agent 模拟常见的浏览器请求
        'Accept': '*/*',  # 接受所有类型的响应
        'Referer': 'https://www.baidu.com',  # 引用来源，模拟从其他页面跳转过来
    }
    
    # 循环请求每一页的搜索结果，最多请求 max_pages 页
    while page_num < max_pages:
        # 构造请求的 URL，使用百度的搜索语法查找目标域名下的子域名
        url = f"https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=site%3A{domain_request}&pn={page_num * 10}"

        try:
            # 发送 HTTP GET 请求获取网页源码，设置超时时间为 10 秒
            resp = requests.get(url, headers=headers, timeout=10)
            
            # 检查请求状态码是否成功
            if resp.status_code != 200:
                print(f"Failed to retrieve page {page_num}, status code: {resp.status_code}")
                # 如果遇到请求过多的情况 (状态码 429)，随机休眠一段时间再继续
                if resp.status_code == 429:
                    print("Too many requests, sleeping for a while...")
                    time.sleep(random.randint(60, 120))  # 随机睡眠 1 到 2 分钟
                break  # 跳出循环，避免进一步请求

            # 使用 BeautifulSoup 解析获取到的网页源码，指定使用 'html.parser' 作为解析器
            soup = BeautifulSoup(resp.content, 'html.parser')

            # 查找所有 class 为 'result' 的 <div> 标签，百度的搜索结果一般包含在这些标签中
            job_bt = soup.find_all('div', attrs={'class': 'result'})

            # 如果没有找到任何结果，结束循环
            if not job_bt:
                print("No more results found.")
                break

            # 遍历查找到的每个 <div> 标签，提取子域名和描述
            for i in job_bt:
                link = i.get('mu')  # 获取 class 为 'result' 的 <div> 标签的 'mu' 属性值，即子域名的链接
                if link:  # 如果链接存在，进一步解析子域名
                    # 使用 urlparse 解析 URL，获取 URL 的协议 (scheme) 和网络位置 (netloc)
                    domain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)
                    # 获取子域名的描述，提取 <h3> 标签内的文本
                    string = i.find('h3').get_text() if i.find('h3') else "No Title"  

                    # 如果解析后的域名已经存在于 Subdomain 列表中则跳过，否则将域名添加到子域名列表中
                    if domain not in Subdomain:
                        Subdomain.append(domain)  # 将新发现的域名加入子域名列表
                        print(f"{domain}\t{string}")  # 打印新发现的域名及其描述
                        found_domains += 1  # 新发现一个域名，计数加 1

            page_num += 1  # 页码加 1，准备抓取下一页
            time.sleep(random.uniform(2, 5))  # 添加随机延时 2 到 5 秒，模拟人工操作

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            # 判断是否是429（Too Many Requests）或其他错误状态码，增加等待时间
            if "429" in str(e) or "403" in str(e):
                print("Detected rate limiting or forbidden access, sleeping for longer...")
                time.sleep(random.randint(180, 300))  # 休眠 3 到 5 分钟再尝试
            else:
                time.sleep(random.randint(30, 60))  # 常规休眠 30 到 60 秒后重试
            continue

    # 汇总打印搜索结果
    print("-----------------------------\n",
          f"对于域名 {domain_request} \n",
          f"共搜索了 {page_num} 页 \n",
          f"共找到 {found_domains} 个子域名。")

# 调用定义的函数，开始收集子域名
# 参数1：目标域名，参数2：要抓取的页数
baidu_search('qq.com', 100)
