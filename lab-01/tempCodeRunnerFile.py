# 定义请求头，绕过反爬机制，模拟浏览器访问
    headers = {
        'User-Agent': ua.random,  # 使用随机的 User-Agent 模拟常见的浏览器请求
        'Accept': '*/*',  # 接受所有类型的响应
        'Referer': 'https://www.baidu.com',  # 引用来源，模拟从其他页面跳转过来
    }