from crypt import methods
from os import lchflags
from flask import Flask, render_template, request

import urllib.request as req
import bs4

app = Flask(__name__)

# 如果你使用 python app.py 指令運行的話也能透過以下程式碼來啟動 flask 。
if __name__ == "__main__":
    app.run()

@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/dating')
def dating():
    return render_template('dating.html')


"""
以下為 Joanne 負責部分
使用者會透過表單回傳三個地點參數中的一個，你需要依照該地點去進行爬蟲。

我提供的變數： 
location = 使用者想爬的地點英文名稱
locationName = 使用者想爬的地點中文名稱

爬蟲回來的資訊應該是一個list，每個list內元素都是一個 dict ，
dict 應有 title 和 url 兩個元素：
 {title: 標題內容放置處, url: 連結放置處} 
完整範例請參考 dummy_results。
可以直接將爬蟲程式碼寫在 def dating_results 函式內，但建議寫在一個獨立的函式裡避免太雜亂
"""
@app.route('/dating', methods=['POST'])
def dating_results():
    location = request.form.get('location')
    if location == 'taipei':
        # 爬台北景點
        locationName = '台北'
        print('爬台北景點')
    elif location == 'taichung':
        # 爬台中景點
        locationName = '台中'
        print('爬台中景點')
    elif location == 'kaohsiung':
        # 爬高雄景點
        locationName = '高雄'
        print('爬高雄景點')

    

    # 假設下列是爬到的資訊
    dummy_results = [{
        'title': '2022 台北約會地點》十大浪漫約會行程，讓你戀情急速加溫',
        'url': 'https://www.klook.com/zh-TW/blog/couple-dating-attractions-taipei-taiwan/'
    }, {
        'title': '2022週末放假玩台北景點|超過50個景點，一日遊行程,親子景點.景觀餐廳.浪漫夜景~超好玩!',
        'url': 'https://fullfenblog.tw/taipei-lazy-bag/'
    }, {
        'title': '台北10 大浪漫活動- 台北最受歡迎的浪漫活動 - Hotels.com',
        'url': 'https://tw.hotels.com/go/taiwan/tw-best-taipei-couples-things-to-do'
    }, {
        'title': '2022台北約會攻略！情侶約會免煩惱，3大浪漫提案為感情增溫！',
        'url': 'https://blog.myfunnow.com/blog/673'
    }, {
        'title': '2022 台北約會景點推薦：情侶約會必去的浪漫夜景＆咖啡廳＆活動清單',
        'url': 'https://blog.pinkoi.com/tw/food-travel/74qrfhjt/'
    }]
    
    return render_template('dating.html', results=dummy_results, bookingValue=location, locationName=locationName)


"""
以下為奕君負責部分
使用者會回傳想要訂房的地點，你需要去爬對應的房型並回傳訂房網站的資訊
格式為 location=想要的地點英文名稱。
location 變數只有三種可能性：taipei, taichung, kaohsiung。

"""

@app.route('/booking', methods=['POST'])
def booking():
    location = request.form.get('bookingLoc')
    return render_template('booking.html', location=location)



@app.route('/gifting')
def gifting():
    return render_template('gifting.html')










""" 以下內容可以不予理會 """

my_list = ['Javascript', 'Python', 'HTML', 'CSS', 'jQuery', 'PHP', 'React.js']
PLATFORMS = ['PChome', "Friday", "Shopee"]
DATA = []
# url = 'https://zhsont.wordpress.com/'

# 舊版，勿用
# @app.route("/")
# def hello_world():
#     return render_template('index.html', plat=PLATFORMS)

# 暫時，之後會去掉
@app.route("/")
def hello_world():
    return render_template('home.html')

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
        # crawPChome(newurl)
        crawl()
    else:
        print('fail!')
    return render_template('result.html', loc=location, pla=platform, gift=gift, history=DATA)
    


def crawl():
    # 初次練習用，這裡面的資訊可以不予理會

    # 抓取我的blog的網頁原始碼
    url = 'https://zhsont.wordpress.com/'

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

    # 解析原始碼，取得每一篇文章的標題
    
    root = bs4.BeautifulSoup(data, "html.parser")
    # print(root.title.string)

    # titles = root.find("h1", class_="entry-title") # 尋找 class="entry-title" 的 h1 標籤
    # print(titles.a.string)

    titles = root.find_all("h5", class_="prod_name")
    for title in titles:
        print(title.a.string)








