from flask import Flask, render_template, redirect
from flask import request as flask_request

import urllib.request as req
import bs4

app = Flask(__name__)



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
    location = flask_request.form.get('location')

    # if location == 'taipei':
        # 爬台北景點


    url="https://www.dcard.tw/topics/%E5%8F%B0%E5%8C%97%E6%99%AF%E9%BB%9E"

    #爬html
    request=req.Request(url,headers={
        #若網站有cookie，也是放這
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    
    
    root=bs4.BeautifulSoup(data,"html.parser")
    #print(root.title.string,"\n")

    list_results=[]

    for title in root.find_all("a",class_="sc-a230363e-3 dsTKss"):
        
        get_title="{}".format(title.text)
        get_url="https://www.dcard.tw"+title.get("href")
        dummy_results = {
            'title': get_title,
            'url': get_url
        }
        list_results.append(dummy_results)


    # elif location == 'taichung':
    #     # 爬台中景點
    #     locationName = '台中'
    #     print('爬台中景點')
    # elif location == 'kaohsiung':
    #     # 爬高雄景點
    #     locationName = '高雄'
    #     print('爬高雄景點')

    

    # 假設下列是爬到的資訊
    # dummy_results = [{
    #     'title': '2022 台北約會地點》十大浪漫約會行程，讓你戀情急速加溫',
    #     'url': 'https://www.klook.com/zh-TW/blog/couple-dating-attractions-taipei-taiwan/'
    # }, {
    #     'title': '2022週末放假玩台北景點|超過50個景點，一日遊行程,親子景點.景觀餐廳.浪漫夜景~超好玩!',
    #     'url': 'https://fullfenblog.tw/taipei-lazy-bag/'
    # }, {
    #     'title': '台北10 大浪漫活動- 台北最受歡迎的浪漫活動 - Hotels.com',
    #     'url': 'https://tw.hotels.com/go/taiwan/tw-best-taipei-couples-things-to-do'
    # }, {
    #     'title': '2022台北約會攻略！情侶約會免煩惱，3大浪漫提案為感情增溫！',
    #     'url': 'https://blog.myfunnow.com/blog/673'
    # }, {
    #     'title': '2022 台北約會景點推薦：情侶約會必去的浪漫夜景＆咖啡廳＆活動清單',
    #     'url': 'https://blog.pinkoi.com/tw/food-travel/74qrfhjt/'
    # }]
    
    return render_template('dating.html', results=list_results, bookingValue='taipei')


"""
以下為奕君負責部分
使用者會回傳想要訂房的地點，你需要去爬對應的房型並回傳訂房網站的資訊
格式為 location=想要的地點英文名稱。
location 變數只有三種可能性：taipei, taichung, kaohsiung。

"""

@app.route('/booking', methods=['POST'])
def booking():
    location = flask_request.form.get('bookingLoc')
    return render_template('booking.html', location=location)



@app.route('/gifting')
def gifting():
    return render_template('gifting.html')

@app.route('/crawl')
def bookingCrawlTest():
    # url = 'https://www.booking.com/searchresults.zh-tw.html?label=gen173nr-1DCAEoggI46AdIM1gEaOcBiAEBmAEwuAEHyAEM2AED6AEBiAIBqAIDuALkn--TBsACAdICJDc2YTkwMmE4LTZiMjUtNGFiNy05OGVlLTllYTM5NWUwOTM3MdgCBOACAQ&sid=ef8c2cbf788afd9c67d94d6da125590a&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.zh-tw.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaOcBiAEBmAEwuAEHyAEM2AED6AEBiAIBqAIDuALkn--TBsACAdICJDc2YTkwMmE4LTZiMjUtNGFiNy05OGVlLTllYTM5NWUwOTM3MdgCBOACAQ%3Bsid%3Def8c2cbf788afd9c67d94d6da125590a%3Bsb_price_type%3Dtotal%26%3B&ss=%E5%8F%B0%E5%8C%97%2C+%E5%8F%B0%E5%8C%97%E5%9C%B0%E5%8D%80%2C+%E8%87%BA%E7%81%A3&is_ski_area=&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=%E5%8F%B0%E5%8C%97&ac_position=0&ac_langcode=xt&ac_click_type=b&dest_id=-2637882&dest_type=city&iata=TPE&place_id_lat=25.046236&place_id_lon=121.51763&search_pageview_id=68a569b2f22c017a&search_selected=true&search_pageview_id=68a569b2f22c017a&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0'
    url = 'https://www.booking.com/searchresults.zh-tw.html?ss=%E5%8F%B0%E5%8C%97&ssne=%E5%8F%B0%E5%8C%97&ssne_untouched=%E5%8F%B0%E5%8C%97&label=gen173nr-1DCAEoggI46AdIM1gEaOcBiAEBmAEwuAEHyAEM2AED6AEBiAIBqAIDuALkn--TBsACAdICJDc2YTkwMmE4LTZiMjUtNGFiNy05OGVlLTllYTM5NWUwOTM3MdgCBOACAQ&sid=ef8c2cbf788afd9c67d94d6da125590a&aid=304142&lang=zh-tw&sb=1&src_elem=sb&src=searchresults&dest_id=-2637882&dest_type=city&checkin=2022-08-15&checkout=2022-08-16&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure'
    price_class = 'fcab3ed991 bd73d13072'
    title_and_img_class = 'b8b0793b0e'
    order_url_class = 'e13098a59f'

    # 建立一個 Request 物件，附加 Request headers 的資訊
    request = req.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    root = bs4.BeautifulSoup(data, "html.parser")

    title_and_img = root.find_all("img", class_=title_and_img_class)
    prices = root.find_all("span", class_=price_class)
    order_portals = root.find_all("a", class_=order_url_class)

    imgurl_list = []
    title_list = []
    results = []

    for entry in title_and_img:
        imgurl_list.append(entry['src'])
        title_list.append(entry['alt'])

    for i in range(len(imgurl_list)):
        new_entry = {}
        new_entry['title'] = title_list[i]
        new_entry['img'] = imgurl_list[i]
        new_entry['price'] = prices[i].string
        new_entry['order'] = order_portals[i]['href']
        results.append(new_entry)

    # print(results)

    # results = dict(zip(booking_com_title_list, booking_com_imgurl_list))
    # print(results)
    return render_template('testcrawl.html', plat='Booking.com', data=results, length=len(results))



[{
    'title':'abc',
    'img': 'ergerger',
    'url': 'ergerger'

},{
    'title':'abc',
    'img': 'ergerger',
    'url': 'ergerger'

},{
    'title':'abc',
    'img': 'ergerger',
    'url': 'ergerger'

}]



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
    return redirect('/home')

@app.route('/result', methods=['POST'])
def result():
    location = flask_request.form.get('location', '台灣')
    platform = flask_request.form.get('platform')
    gift = flask_request.form.get('gift')
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

# 如果你使用 python app.py 指令運行的話也能透過以下程式碼來啟動 flask 。
if __name__ == "__main__":
    app.run()






