from flask import Flask, render_template, redirect
from flask import request as flask_request

app = Flask(__name__)




@app.route("/") # url 端點
def hello_world(): # 觸發 hello_world 函式
    return render_template('/home.html') # 回傳 HTML 檔案




@app.route("/result", methods=['POST']) # 此 url 端點只接受 POST request
def result(): # 觸發 result 函式
    location = flask_request.form.get('location') # 將傳送至 /result 的 location 表單資料儲存為變數
    return redirect('/result.html', var=location) # 回傳 HTML 檔案以及 var 變數到前端






Flask
render_template
redirect
