from flask import Flask, render_template, redirect
from flask import request as flask_request

import requests, json

import urllib.request as req
import ssl
import bs4

# wordcloud
import jieba
jieba.load_userdict('static/dict.txt.big')
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import os
import random

app = Flask(__name__)


# 暫時，之後會去掉
@app.route("/")
def hello_world():
    return redirect('/home')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/dating')
def dating():
    return render_template('dating.html')

@app.route('/dating', methods=['POST'])
def dating_results():
    location = flask_request.form.get('location')


    print(f'location= {location}')

    if location == 'taipei':
        url="https://www.dcard.tw/topics/%E5%8F%B0%E5%8C%97%E6%99%AF%E9%BB%9E"
    elif location =='taichung':
        url='https://www.dcard.tw/topics/%E5%8F%B0%E4%B8%AD%E6%99%AF%E9%BB%9E'
    elif location == 'tainan':
        url='https://www.dcard.tw/topics/%E5%8F%B0%E5%8D%97%E6%99%AF%E9%BB%9E'
    elif location == 'kaohsiung':
        url='https://www.dcard.tw/topics/%E9%AB%98%E9%9B%84%E6%99%AF%E9%BB%9E'
    
    print(f'url={url}')

    #爬html
    request=req.Request(url,headers={
        #若網站有cookie，也是放這
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    })

    # 選擇不用認證此 SSL 憑證
    ssl._create_default_https_context = ssl._create_unverified_context

    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    
    root=bs4.BeautifulSoup(data,"html.parser")
    #print(root.title.string,"\n")

    list_results=[]

    # ~~~新方法~~~
    for new_a in root.find_all("article"):
        new_h2 = new_a.find("h2")
        new_a2 = new_h2.find("a")
        new_title = new_a2.text
        new_url="https://www.dcard.tw"+new_a2.get("href")
        results = {
            'title': new_title,
            'url': new_url
        }
        
        list_results.append(results)
    # print('接下來是用新方法取得到Dcard的標題：', list_results)
    # ~~~新方法~~~


    # ~~~舊方法~~~
    # for title in root.find_all("a",class_="sc-a230363e-3 dsTKss"): # sc-b205d8ae-3 iOQsOu
        
    #     get_title="{}".format(title.text)
    #     get_url="https://www.dcard.tw"+title.get("href")
    #     dummy_results = {
    #         'title': get_title,
    #         'url': get_url
    #     }
    #     list_results.append(dummy_results)
    
    # print(f'list results={list_results}')
    # ~~~舊方法~~~


    return render_template('dating.html', results=list_results, bookingValue='taipei')
    # return render_template('dating.html')


@app.route('/booking', methods=['POST'])
def booking():
   # year1=str(input("輸入西元年:"))
   # month1=str(input("輸入月(01、02...)"))
   # date1=str(input("輸入日(01、02...)"))
   # year2=str(input("輸入西元年:"))
   # month2=str(input("輸入月(01、02...)"))
   # date2=str(input("輸入日(01、02...)"))
    price_class = 'fcab3ed991 bd73d13072'
    title_and_img_class = 'b8b0793b0e'
    order_url_class = 'e13098a59f'
    #url=f"https://www.booking.com/searchresults.zh-tw.html?label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&ss=%E5%8F%B0%E5%8C%97&ssne=%E5%8F%B0%E5%8C%97&ssne_untouched=%E5%8F%B0%E5%8C%97&lang=zh-tw&sb=1&src_elem=sb&dest_id=-2637882&dest_type=city&checkin={year1}-{month1}-{date1}&checkout={year2}-{month2}-{date2}&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&order=class"
    #試用URL
    url="https://www.booking.com/searchresults.zh-tw.html?label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&ss=%E5%8F%B0%E5%8C%97&ssne=%E5%8F%B0%E5%8C%97&ssne_untouched=%E5%8F%B0%E5%8C%97&lang=zh-tw&sb=1&src_elem=sb&dest_id=-2637882&dest_type=city&checkin=2022-08-02&checkout=2022-08-05&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&order=class"
    request = req.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
        
    root = bs4.BeautifulSoup(data, "html.parser")

    title_and_img = root.find_all("img", class_=title_and_img_class)
    prices = root.find_all("span", class_=price_class)
    order_portals = root.find_all("a", class_=order_url_class)
    money=root.find_all("span",class_='fcab3ed991 bd73d13072')
    score=root.find_all('div',class_='b5cd09854e d10a6220b4')

    imgurl_list = []
    title_list = []
    results = []
    money_text=[]
    score_text=[]


    for M in money:
        money_text.append(M.text)

    for S in score:
        score_text.append(S.text)   
        
    for entry in title_and_img:
        imgurl_list.append(entry['src'])
        title_list.append(entry['alt'])

    money_list=[]
    for j in range(len(money_text)):
        Mtext=money_text[j].replace(u'\xa0', ' ')
        money_list=money_list+[Mtext]

    score=root.find_all('div',class_='b5cd09854e d10a6220b4')
    score_C=[]
    for S in range(len(score_text)):
        Stext=score_text[S].replace(u'\xa0', ' ')
        
        score_C=score_C+[Stext]

    score_list=[]
    for T in range(len(score_C)):
        score_n="評分:"+score_C[T]+"分"
        score_list=score_list+[score_n]

    for i in range(len(imgurl_list)):
            new_entry = {}
            new_entry['title'] = title_list[i]
            new_entry['img'] = imgurl_list[i]
            new_entry['price'] = prices[i].string
            new_entry['order'] = order_portals[i]['href']
            new_entry["score"] =score_list[i]
            results.append(new_entry)

    

    location = flask_request.form.get('bookingLoc')
    return render_template('booking.html', data=results)

@app.route('/gifting')
def gifting():
    return render_template('gifting.html', keyword='', data='!initial')

# 在全域宣告「先前圖片名稱」
prevname = 'output'

@app.route('/gifting', methods=['POST'])
def gifting_results():

    global prevname
    # 先把舊的文字雲刪掉
    if os.path.exists(f"static/wordcloud/{prevname}.jpg"):
        os.remove(f'static/wordcloud/{prevname}.jpg')

    randname = str(random.random())[2:8]
    
    # 將本次名稱儲存到「先前圖片名稱」
    prevname = randname
    imgpath = f"static/wordcloud/{randname}.jpg"
    

    keyword = flask_request.form.get('keyword')
    # 防呆機制
    if (keyword.strip() == ''):
        results = ''
    else:
        results = shopee_crawler(keyword, randname)

    return render_template('gifting.html', data=results, keyword=keyword, imgname=imgpath)


@app.route('/crawl')
def bookingCrawlTest():
    # url = 'https://www.booking.com/searchresults.zh-tw.html?label=gen173nr-1DCAEoggI46AdIM1gEaOcBiAEBmAEwuAEHyAEM2AED6AEBiAIBqAIDuALkn--TBsACAdICJDc2YTkwMmE4LTZiMjUtNGFiNy05OGVlLTllYTM5NWUwOTM3MdgCBOACAQ&sid=ef8c2cbf788afd9c67d94d6da125590a&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.zh-tw.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaOcBiAEBmAEwuAEHyAEM2AED6AEBiAIBqAIDuALkn--TBsACAdICJDc2YTkwMmE4LTZiMjUtNGFiNy05OGVlLTllYTM5NWUwOTM3MdgCBOACAQ%3Bsid%3Def8c2cbf788afd9c67d94d6da125590a%3Bsb_price_type%3Dtotal%26%3B&ss=%E5%8F%B0%E5%8C%97%2C+%E5%8F%B0%E5%8C%97%E5%9C%B0%E5%8D%80%2C+%E8%87%BA%E7%81%A3&is_ski_area=&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=%E5%8F%B0%E5%8C%97&ac_position=0&ac_langcode=xt&ac_click_type=b&dest_id=-2637882&dest_type=city&iata=TPE&place_id_lat=25.046236&place_id_lon=121.51763&search_pageview_id=68a569b2f22c017a&search_selected=true&search_pageview_id=68a569b2f22c017a&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0'
    #url = 'https://www.booking.com/searchresults.zh-tw.html?ss=%E5%8F%B0%E5%8C%97&ssne=%E5%8F%B0%E5%8C%97&ssne_untouched=%E5%8F%B0%E5%8C%97&label=gen173nr-1DCAEoggI46AdIM1gEaOcBiAEBmAEwuAEHyAEM2AED6AEBiAIBqAIDuALkn--TBsACAdICJDc2YTkwMmE4LTZiMjUtNGFiNy05OGVlLTllYTM5NWUwOTM3MdgCBOACAQ&sid=ef8c2cbf788afd9c67d94d6da125590a&aid=304142&lang=zh-tw&sb=1&src_elem=sb&src=searchresults&dest_id=-2637882&dest_type=city&checkin=2022-08-15&checkout=2022-08-16&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure'
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


def shopee_crawler(keyword, randname): # 可以放參數進去

    url = 'https://shopee.tw/api/v4/search/search_items?by=sales&keyword=' + keyword + '&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'
    
    res = requests.get(url, headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'})
    
    resjson = json.loads(res.text)
    
    gift_list = []
    
    for outcome in resjson['items']:
        name = outcome['item_basic']['name']
        historical_sold = outcome['item_basic']['historical_sold']
    
        if outcome['item_basic']['price_min'] == outcome['item_basic']['price_max']:
            price = str(int(outcome['item_basic']['price_min']/100000))
        else:
            price = str(int(outcome['item_basic']['price_min']/100000)) + '~' + str(int(outcome['item_basic']['price_max']/100000))
              
        image = 'https://cf.shopee.tw/file/' + outcome['item_basic']['image']
    
        website = 'https://shopee.tw/' + outcome['item_basic']['name'].replace(' ', '-') + '-i.' + str(outcome['item_basic']['shopid']) + '.' + str(outcome['item_basic']['itemid'])

        shopee_dict = {'name' : name,
                       'historical_sold' : historical_sold,
                       'price' : price,
                       'image' : image,
                       'website' : website}
        
        gift_list.append(shopee_dict)


    cleaned = []

    for outcome in resjson['items']:

        cleaned.append(outcome['item_basic']['name'])
        
    articleAll = '\n'.join(cleaned)
    articleAll.replace('\n', '')
    
    stopwords = {}.fromkeys(['也', '日', '月', '人', '在', '是', '的', '4', '5', '，', '、', ',', '!', '2', '3',
                        '2022', '12', '2', '「', '」', '(', ')', '！', '（', '）', '。', '/', '／', '?','【', '】'])
    
    Sentence = jieba.cut_for_search(articleAll)

    hash = {}
    for item in Sentence:
    
        if item in stopwords:
            continue
        
        if item in hash:
            hash[item] +=1
        else:
            hash[item] = 1

    bgimage = np.array(Image.open("static/heart.png"))

        
    wc = WordCloud(font_path = 'static/SNsanafonkaku.ttf',
                   background_color = 'white',
                   max_words = 500,
                   stopwords = stopwords,
                   mask = bgimage)

    # 使用dictionary的內容產生文字
    wc.generate_from_frequencies(hash)

    # 視覺化呈現

    # plt.imshow(wc)
    # plt.axis('off')
    # plt.figure(figsize=(50, 50), dpi = 600)
    # plt.show()

    
    wc.to_file(f'static/wordcloud/{randname}.jpg')


    # print(gift_list)
    return gift_list
        
    # shopee_crawler(keyword)

# 如果你使用 python app.py 指令運行的話也能透過以下程式碼來啟動 flask 。
if __name__ == "__main__":
     app.run(debug=True, port=5001)







# def crawPChome(newurl):
#     # 測試爬PChome

#     # 建立一個 Request 物件，附加 Request headers 的資訊
#     print('1')
#     request = req.Request(newurl, headers={
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
#     })
#     with req.urlopen(request) as response:
#         data = response.read().decode("utf-8")
#     # print(data)

#     # 解析原始碼，取得每一篇文章的標題
    
#     root = bs4.BeautifulSoup(data, "html.parser")
#     # print(root.title.string)

#     # titles = root.find("h1", class_="entry-title") # 尋找 class="entry-title" 的 h1 標籤
#     # print(titles.a.string)

#     titles = root.find_all("h5", class_="prod_name")
#     for title in titles:
#         print(title.a.string)


# def crawl():
#     # 初次練習用，這裡面的資訊可以不予理會

#     # 抓取我的blog的網頁原始碼
#     url = 'https://zhsont.wordpress.com/'

#     # 建立一個 Request 物件，附加 Request headers 的資訊
#     request = req.Request(url, headers={
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
#     })
#     with req.urlopen(request) as response:
#         data = response.read().decode("utf-8")
#     # print(data)

#     # 解析原始碼，取得每一篇文章的標題
    
#     root = bs4.BeautifulSoup(data, "html.parser") # 讓 Beautifulsoup 解析 HTML 文件
#     # print(root.title.string)

#     # titles = root.find("h1", class_="entry-title") # 尋找 class="entry-title" 的 h1 標籤
#     # print(titles.a.string)

#     titles = root.find_all("h1", class_="entry-title")
#     for title in titles:
#         print(title.a.string)

# @app.route('/result', methods=['POST'])
# def result():
#     location = flask_request.form.get('location', '台灣')
#     platform = flask_request.form.get('platform')
#     gift = flask_request.form.get('gift')
#     new_entry = {'name': location, 'plat': platform, 'gift':gift}
#     DATA.append(new_entry)


#     if platform == "PChome":
#         newurl = 'https://ecshweb.pchome.com.tw/search/v3.3/?q=' + gift
#         print(newurl)
#         # crawPChome(newurl)
#         crawl()
#     else:
#         print('fail!')
#     return render_template('result.html', loc=location, pla=platform, gift=gift, history=DATA)
    