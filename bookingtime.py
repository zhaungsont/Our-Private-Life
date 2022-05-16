from flask import Flask, render_template, request, redirect

import urllib.request as req
import bs4
from flask import request
import re


year1=str(input("輸入西元年:"))
month1=str(input("輸入月(01、02...)"))
date1=str(input("輸入日(01、02...)"))
year2=str(input("輸入西元年:"))
month2=str(input("輸入月(01、02...)"))
date2=str(input("輸入日(01、02...)"))
url=f"https://www.booking.com/searchresults.zh-tw.html?label=booking-name-yefrPbbyS*FIINHgyCnmNgS267725091255%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1012825%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=f403d2b3a73243d32c27dbfc3fa9f606&aid=376396&ss=%E5%8F%B0%E5%8C%97&ssne=%E5%8F%B0%E5%8C%97&ssne_untouched=%E5%8F%B0%E5%8C%97&lang=zh-tw&sb=1&src_elem=sb&dest_id=-2637882&dest_type=city&checkin={year1}-{month1}-{date1}&checkout={year2}-{month2}-{date2}&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&order=class"
print(url)
price_class = 'fcab3ed991 bd73d13072'
title_and_img_class = 'b8b0793b0e'
order_url_class = 'e13098a59f'

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

imgurl_list = []
title_list = []
results = []
money_text=[]

for M in money:
    money_list.append(M.text)

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

money_list=[]
for j in range(len(money_text)):
    Mtext=money_text[j].replace(u'\xa0', ' ')
    money_list=money_list+[Mtext]
print(money_list)

score=root.find_all('div',class_='b5cd09854e d10a6220b4')
score_C=[]
for S in range(len(score_text)):
    Stext=score_text[S].replace(u'\xa0', ' ')
    
    score_C=score_C+[Stext]
print(score_C)

score_list=[]
for T in range(len(score_C)):
    score_n="評分:"+score_C[T]+"分"
    score_list=score_list+[score_n]
print(score_list)