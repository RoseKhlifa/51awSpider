from bs4 import BeautifulSoup
import requests
key = input("[!]输入搜索关键字:")
limit_raw = input("[!]输入搜索结果限制数(回车=不限制):").strip()
limit = int(limit_raw) if limit_raw else 0   # 0 表示不限制
url = "https://51aw.com/search/"+key+"/1"#请求地址
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"}#伪装user-agent
response = requests.get(url=url,headers=headers) #发送请求
print(response.status_code)
if(response.status_code == 200):
    print("[+]关键字搜索成功")
else:
    print("[+]关键字搜索失败")
    exit()
#此处是在实例化BeautifulSoup对象 用=来实例化
soup = BeautifulSoup(response.text,'lxml')#第二个参数是解析器
#print(soup.find('body')) #FIND方法 查找某个标签(遇见第一个就返回了)  FIND_ALL方法 查找所有标签(返回列表)
#print(soup.find(attrs={"id":"content"})) #通过属性查找标签
#print(soup.find(attrs={"class":"article"})) #通过属性查找标签
#soup.find()返回的是tag对象，可以继续调用find方法
pageInfo = soup.find(name='span',attrs={"class":"page-current"})
pageinfo_text = pageInfo.get_text(strip=True)   # 去首尾空白
current_page, total_page = map(int, pageinfo_text.split('/'))
count = 0  # 已抓取文章数
stop_all = False
for i in range (1,total_page+1): #左闭右开
    url = "https://51aw.com/search/"+key+"/"+str(i)
    new_response = requests.get(url=url,headers=headers)
    print("[+]当前页:",i,"总页数:",total_page)
    if(new_response.status_code == 200):
        print("[+]该页进入成功")
    else:
        print("[-]该页进入失败")
        exit()
    new_soup = BeautifulSoup(new_response.text,'lxml')
    div = new_soup.find_all(name='div',attrs={"id":"archive","role":"main"}) #查找div标签
    article = div[0].find_all(name='article') #在div标签下查找article标签
    j = 1
    for tag in article:
        if limit and count >= limit:
            stop_all = True
            break
        a = tag.find(name='a')
        link = a.get('href')
        title = a.find(name='h2').text
        print("[+]",j,".标题:",title,"链接:",link)
        newnew_response = requests.get(url=link,headers=headers)
        if(newnew_response.status_code == 200):
            print("[+]该篇文章获取成功")
        else:
            print("[-]该篇文章获取失败")
            exit()
        newnew_soup = BeautifulSoup(newnew_response.text,'lxml')
        post = newnew_soup.find(name='div',attrs={"class":"post-content"})
        if not post:
            print("[-]未找到 post-content，跳过")
            j += 1
            continue
        for bq in post.find_all("blockquote"):
            bq.decompose()
        texts = []
        for p in post.find_all("p"):
        # 删除 p 内的 img，防止 alt/title 混入文本
            for img in p.find_all("img"):
                img.decompose()
            txt = p.get_text(strip=True)
            if not txt:
                continue
            if "全网最全的吃瓜网站，禁制级猎奇资源无限制免费观看" in txt:
                break
            texts.append(txt)
        final_text = "\n".join(texts)
        print(final_text)     
        count += 1
        j += 1
    if stop_all:
        break

