from crypt import methods
from flask import Flask, render_template, request

app = Flask(__name__)

my_list = ['Javascript', 'Python', 'HTML', 'CSS', 'jQuery', 'PHP', 'React.js']
PLATFORMS = ['PChome', "Friday", "Shopee"]
DATA = []

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
    return render_template('result.html', loc=location, pla=platform, gift=gift, history=DATA)
    

