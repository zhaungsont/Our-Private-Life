from crypt import methods
from flask import Flask, render_template, request

import urllib.request as req
import bs4

app = Flask(__name__)

my_list = ['Javascript', 'Python', 'HTML', 'CSS', 'jQuery', 'PHP', 'React.js']
PLATFORMS = ['PChome', "Friday", "Shopee"]
DATA = []
url = 'https://zhsont.wordpress.com/'


@app.route("/")
def hello_world():
    return render_template('index.html', plat=PLATFORMS)

@app.route('/result', methods=['POST'])
def result():
    location = request.form.get('location', '台灣')
    platform = request.form.get('platform')
    gift = request.form.get('gift')
    new_entry = {'name': location, 'plat': platform, 'gift':gift}
    DATA.append(new_entry)


    if platform == "PChome":
        newurl = 'https://ecshweb.pchome.com.tw/search/v3.3/?q=' + gift
        print(newurl)
        crawPChome(newurl)
    else:
        print('fail!')
    return render_template('result.html', loc=location, pla=platform, gift=gift, history=DATA)
    
def crawl():
    # 初次練習用，這裡面的資訊可以不予理會

    # 抓取我的blog的網頁原始碼
    # url = 'https://zhsont.wordpress.com/'

    # 建立一個 Request 物件，附加 Request headers 的資訊
    request = req.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    # print(data)

    # 解析原始碼，取得每一篇文章的標題
    
    root = bs4.BeautifulSoup(data, "html.parser") # 讓 Beautifulsoup 解析 HTML 文件
    # print(root.title.string)

    # titles = root.find("h1", class_="entry-title") # 尋找 class="entry-title" 的 h1 標籤
    # print(titles.a.string)

    titles = root.find_all("h1", class_="entry-title")
    for title in titles:
        print(title.a.string)

def crawPChome(newurl):
    # 測試爬PChome

    # 建立一個 Request 物件，附加 Request headers 的資訊
    print('1')
    request = req.Request(newurl, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    # print(data)
    print('2')

    # 解析原始碼，取得每一篇文章的標題
    
    root = bs4.BeautifulSoup(data, "html.parser")
    # print(root.title.string)
    print('3')

    # titles = root.find("h1", class_="entry-title") # 尋找 class="entry-title" 的 h1 標籤
    # print(titles.a.string)

    titles = root.find_all("h5", class_="prod_name")
    for title in titles:
        print(title.a.string)