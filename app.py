# flask
from flask import Flask, render_template, redirect
from flask import request as flask_request

# web scraping
import requests, json
import urllib.request as req
from bs4 import BeautifulSoup


import os
import random

# wordcloud
import jieba
jieba.load_userdict('static/dict.txt.big')
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  

app = Flask(__name__)

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
    temp, temp_desc = weather(location)
    print(temp)
    print(temp_desc)

    if location == 'taipei':
        loc_name = '台北'
        url="https://www.dcard.tw/topics/%E5%8F%B0%E5%8C%97%E6%99%AF%E9%BB%9E"
    elif location == 'newtaipei':
        loc_name = '新北'
        url='https://www.dcard.tw/search/posts?forum=travel&query=%E6%96%B0%E5%8C%97%E5%B8%82%E6%99%AF%E9%BB%9E'
    elif location == 'yilan':
        loc_name = '宜蘭'
        url='https://www.dcard.tw/search/posts?forum=travel&query=%E5%AE%9C%E8%98%AD&sort=relevance'
    elif location == 'hualiang':
        loc_name = '花蓮'
        url='https://www.dcard.tw/topics/%E8%8A%B1%E8%93%AE%E6%99%AF%E9%BB%9E'
    elif location == 'taidung':
        loc_name = '台東'
        url='https://www.dcard.tw/topics/%E5%8F%B0%E6%9D%B1%E6%99%AF%E9%BB%9E'
    elif location =='taichung':
        loc_name = '台中'
        url='https://www.dcard.tw/topics/%E5%8F%B0%E4%B8%AD%E6%99%AF%E9%BB%9E'
    elif location == 'miaoli':
        loc_name = '苗栗'
        url='https://www.dcard.tw/topics/%E8%8B%97%E6%A0%97?forums=travel'
    elif location == 'tainan':
        loc_name = '台南'
        url='https://www.dcard.tw/topics/%E5%8F%B0%E5%8D%97%E6%99%AF%E9%BB%9E'
    elif location == 'kaohsiung':
        loc_name = '高雄'
        url='https://www.dcard.tw/topics/%E9%AB%98%E9%9B%84%E6%99%AF%E9%BB%9E'
    elif location == 'pingtung':
        loc_name = '屏東'
        url='https://www.dcard.tw/topics/%E5%B1%8F%E6%9D%B1?forums=travel'


    print(f'url={url}')

    #爬html
    request=req.Request(url,hdrs={
        #若網站有cookie，也是放這
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    })

    # 選擇不用認證此 SSL 憑證
    # ssl._create_default_https_context = ssl._create_unverified_context

    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    
    root=BeautifulSoup(data,"html.parser")
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

    #我只要十筆就好！！
    list_results = list_results[0:10]

    return render_template('dating.html', results=list_results, bookingValue=location, locationName=loc_name, temp=temp, temp_desc=temp_desc)

    
def weather(loc):

    # driverPath='static/chromedriver'
    # browser=webdriver.Chrome(driverPath)
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  

    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path='static/selenium/chromedriver')  


    url='https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=63'
    browser.get(url)

    s=Select(browser.find_element(By.ID,'CID'))
    if loc=='taipei':
        s.select_by_value("63") #選擇縣市
    elif loc == 'newtaipei':
        s.select_by_value("65") #選擇縣市
    elif loc == 'yilan':
        s.select_by_value("10002") #選擇縣市
    elif loc == 'hualiang':
        s.select_by_value("10015") #選擇縣市
    elif loc == 'taidung':
        s.select_by_value("10014") #選擇縣市
    elif loc =='taichung':
        s.select_by_value("66") #選擇縣市
    elif loc == 'miaoli':
        s.select_by_value("10005") #選擇縣市
    elif loc == 'tainan':
        s.select_by_value("67") #選擇縣市
    elif loc == 'kaohsiung':
        s.select_by_value("64") #選擇縣市
    elif loc == 'pingtung':
        s.select_by_value("10013") #選擇縣市

    soup=BeautifulSoup(browser.page_source,'html.parser')
    temperature=soup.select_one('li:nth-child(2)>span.tem>span.tem-C.is-active').text
    info=browser.find_element(By.XPATH, "//*[@id='marquee_1']").text 
    new_info=info.replace('\n看更多','')

    #results=
    print(temperature) #所選縣市氣溫
    print(new_info) #所選縣市天氣狀況

    return [temperature, new_info]


@app.route("/booking_select",methods=['POST','GET'])
def booking_people():
    loc = flask_request.form.get("bookingLoc")
    locName = flask_request.form.get("locationName")

    #loc 抓取 bookingLoc 資料
    #bookingLoc 來自 booking.html input type="hidden"
    return render_template('booking_select.html',bookingLoc=loc, locName=locName)
    #returm 到booking_select.html 並將 loc 抓到的資料丟到booking_select.html


@app.route('/booking', methods=['POST','GET'])
def booking():
    #將 booking_select.html 選擇的數據回傳並儲存在各自的變數內
    location = flask_request.form.get('bookingLoc')
    year1 = flask_request.form.get('check_in_year')
    month1 = flask_request.form.get('check_in_month')
    date1= flask_request.form.get('check_in_date')
    year2 = flask_request.form.get('check_out_year')
    month2 = flask_request.form.get('check_out_month')
    date2= flask_request.form.get('check_out_date')
    ad = flask_request.form.get('ad')
    ch = flask_request.form.get('ch')
    room = flask_request.form.get('room')
    #在終端機輸出 確保資料抓取正確

    cat = f'checkin={year1}-{month1}-{date1}&checkout={year2}-{month2}-{date2}&group_adults={ad}&no_rooms={room}&group_children={ch}&sb_travel_purpose=leisure'
    
    if location == 'taipei':
        url = 'https://www.booking.com/searchresults.zh-tw.html?ss=%E5%8F%B0%E5%8C%97&ssne=%E5%8F%B0%E5%8C%97&ssne_untouched=%E5%8F%B0%E5%8C%97&label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&lang=zh-tw&sb=1&src_elem=sb&src=searchresults&dest_id=-2637882&dest_type=city&' + cat
    elif location == 'newtaipei':
        url = 'https://www.booking.com/searchresults.zh-tw.html?ss=%E6%96%B0%E5%8C%97%E5%B8%82%2C+%E5%8F%B0%E6%B9%BE&ssne=%E5%8F%B0%E5%8C%97&ssne_untouched=%E5%8F%B0%E5%8C%97&label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&lang=zh-tw&sb=1&src_elem=sb&src=searchresults&dest_id=5245&dest_type=region&ac_position=0&ac_click_type=b&ac_langcode=zh&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=347f4713a16703de&' + cat
    elif location == 'yilan':
        url = 'https://www.booking.com/searchresults.zh-tw.html?ss=%E5%AE%9C%E8%98%AD&ssne=%E6%96%B0%E5%8C%97%E5%B8%82&ssne_untouched=%E6%96%B0%E5%8C%97%E5%B8%82&label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&lang=zh-tw&sb=1&src_elem=sb&src=searchresults&dest_id=5238&dest_type=region&ac_position=0&ac_click_type=b&ac_langcode=xt&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=c8044752c4fe0421&' + cat
    elif location == 'hualiang':
        url='https://www.booking.com/searchresults.zh-tw.html?ss=%E8%8A%B1%E8%93%AE%E5%B8%82%2C+%E8%8A%B1%E8%93%AE%E7%B8%A3%2C+%E8%87%BA%E7%81%A3&ssne=%E5%AE%9C%E8%98%AD%E7%B8%A3&ssne_untouched=%E5%AE%9C%E8%98%AD%E7%B8%A3&label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&lang=zh-tw&sb=1&src_elem=sb&src=searchresults&dest_id=-2631690&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=xt&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=fed64785bfba040a&' + cat
    elif location == 'taidung':
        url='https://www.booking.com/searchresults.zh-tw.html?ss=%E5%8F%B0%E6%9D%B1%E5%B8%82%2C+%E5%8F%B0%E6%9D%B1%E7%B8%A3%2C+%E8%87%BA%E7%81%A3&ssne=%E8%8A%B1%E8%93%AE%E5%B8%82&ssne_untouched=%E8%8A%B1%E8%93%AE%E5%B8%82&label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&lang=zh-tw&sb=1&src_elem=sb&src=searchresults&dest_id=-2637928&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=xt&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=f80a48a1417e004e&' + cat
    elif location =='taichung':
        url='https://www.booking.com/searchresults.zh-tw.html?ss=%E5%8F%B0%E4%B8%AD%E5%B8%82%2C+%E5%8F%B0%E4%B8%AD%E5%9C%B0%E5%8C%BA%2C+%E5%8F%B0%E6%B9%BE&ssne=%E5%8F%B0%E6%9D%B1%E5%B8%82&ssne_untouched=%E5%8F%B0%E6%9D%B1%E5%B8%82&label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&lang=zh-tw&sb=1&src_elem=sb&src=searchresults&dest_id=-2637824&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=zh&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=391048ad40ef0919&' + cat
    elif location == 'miaoli':
        url='https://www.booking.com/searchresults.zh-tw.html?ss=%E8%8B%97%E6%A0%97%E5%8E%BF%2C+%E5%8F%B0%E6%B9%BE&ssne=%E5%8F%B0%E4%B8%AD&ssne_untouched=%E5%8F%B0%E4%B8%AD&label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&lang=zh-tw&sb=1&src_elem=sb&src=searchresults&dest_id=5240&dest_type=region&ac_position=0&ac_click_type=b&ac_langcode=zh&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=a07748bca8120782&checkin=2022-07-01&' + cat
    elif location == 'tainan':
        url='https://www.booking.com/searchresults.zh-tw.html?ss=%E5%8F%B0%E5%8D%97%2C+%E5%8F%B0%E5%8D%97%E5%9C%B0%E5%8C%BA%2C+%E5%8F%B0%E6%B9%BE&ssne=%E8%8B%97%E6%A0%97%E7%B8%A3&ssne_untouched=%E8%8B%97%E6%A0%97%E7%B8%A3&label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&lang=zh-tw&sb=1&src_elem=sb&src=searchresults&dest_id=-2637868&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=zh&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=931e48c6582b0282&checkin=2022-07-01&' + cat
    elif location == 'kaohsiung':
        url='https://www.booking.com/searchresults.zh-tw.html?ss=%E9%AB%98%E9%9B%84%2C+%E9%AB%98%E9%9B%84%E5%9C%B0%E5%8C%BA%2C+%E5%8F%B0%E6%B9%BE&ssne=%E5%8F%B0%E5%8D%97&ssne_untouched=%E5%8F%B0%E5%8D%97&label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&lang=zh-tw&sb=1&src_elem=sb&src=searchresults&dest_id=-2632378&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=zh&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=8a4048d33827001b&checkin=2022-07-01&' + cat
    elif location == 'pingtung':
        url='https://www.booking.com/searchresults.zh-tw.html?ss=%E5%B1%8F%E6%9D%B1%E5%B8%82%2C+%E5%B1%8F%E6%9D%B1%E7%B8%A3%2C+%E8%87%BA%E7%81%A3&ssne=%E9%AB%98%E9%9B%84&ssne_untouched=%E9%AB%98%E9%9B%84&label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&lang=zh-tw&sb=1&src_elem=sb&src=searchresults&dest_id=-2635731&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=xt&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=706e48e23612046a&checkin=2022-07-01&' + cat
    else:
        location = 'error'
    
    # print(location)
    # print(year1)
    # print(month1)
    # print(date1)
    # print(year2)
    # print(month2)
    # print(date2)
    # print(ad)
    # print(ch)
    # print(room)
    #將變數帶入 url 內 並用此 url 進行爬蟲

    # endodedLoc = urllib.parse.quote(location, safe='&=')

    # url=f"https://www.booking.com/searchresults.zh-tw.html?ss={endodedLoc}&label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&ss=%E5%8F%B0%E5%8C%97&ssne=%E5%8F%B0%E5%8C%97&ssne_untouched=%E5%8F%B0%E5%8C%97&lang=zh-tw&sb=1&src_elem=sb&dest_id=-2637882&dest_type=city&checkin={year1}-{month1}-{date1}&checkout={year2}-{month2}-{date2}&group_adults={ad}&no_rooms={room}&group_children={ch}&sb_travel_purpose=leisure&order=class"
    print("***********")
    print(url)
    print("***********")


    #booking網頁內部要抓取的目標標籤名稱
    price_class = 'fcab3ed991 bd73d13072'
    title_and_img_class = 'b8b0793b0e'
    order_url_class = 'e13098a59f'
    #爬蟲抓取
    request = req.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    })
    #取的網頁的原始碼 並用decode("utf-8")來翻譯成中文
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    #解析方法
    root = BeautifulSoup(data, "html.parser")
    #抓取對應標籤之資料
    title_and_img = root.find_all("img", class_=title_and_img_class)
    prices = root.find_all("span", class_=price_class)
    order_portals = root.find_all("a", class_=order_url_class)
    money=root.find_all("span",class_='fcab3ed991 bd73d13072')
    score=root.find_all('div',class_='b5cd09854e d10a6220b4')
    #設定空list
    imgurl_list = []
    title_list = []
    results = []
    money_text=[]
    score_text=[]

    #將變數 money 資料放入 money_text list
    for M in money:
        money_text.append(M.text)
    #將變數 score 資料放入 score_text list
    for S in score:
        score_text.append(S.text)   
    #將變數 title_and_img 資料放入 imgurl_list & title_list
    for entry in title_and_img:
        imgurl_list.append(entry['src'])
        title_list.append(entry['alt'])
    #抓取價錢資料
    money_list=[]
    #根據 money_text 長度判斷跑幾次 將\xa0取代為空白
    # money_text 放入 money_list
    for j in range(len(money_text)):
        Mtext=money_text[j].replace(u'\xa0', ' ')
        money_list=money_list+[Mtext]
    #抓取評價資料
    score=root.find_all('div',class_='b5cd09854e d10a6220b4')
    score_C=[]
    #根據 score_text 長度判斷跑幾次 將\xa0取代為空白
    for S in range(len(score_text)):
        Stext=score_text[S].replace(u'\xa0', ' ')
        
        score_C=score_C+[Stext]
    #將評價資料加上文字
    score_list=[]
    for T in range(len(score_C)):
        score_n="評分:"+score_C[T]+"分"
        score_list=score_list+[score_n]
    #將所有抓取到的資料list 照順序存進字典 new_entry
    for i in range(len(imgurl_list)):
        new_entry = {}
        new_entry['title'] = title_list[i]
        new_entry['img'] = imgurl_list[i]
        new_entry['order'] = order_portals[i]['href']
        try:
            new_entry['price'] = prices[i].string
        except:
            new_entry['price'] = '點擊連結以觀看'
        try:
            new_entry["score"] =score_list[i]
        except:
            new_entry["score"] ='尚無評價'
        results.append(new_entry)

    #將資料return到booking.html        
    return render_template('booking.html', data=results, year1=year1, month1=month1, date1=date1, year2=year2, month2=month2, date2=date2, ad=ad, ch=ch, room=room)


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
        

# 如果你使用 python app.py 指令運行的話也能透過以下程式碼來啟動 flask 。
if __name__ == "__main__":
     app.run(debug=True, port=5001)

