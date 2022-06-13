# 我們的私生活 Our Private Life

「我們的私生活」能協助用戶查找台灣熱門景點的介紹、天氣以及住宿資訊，也提供一站式禮物搜尋功能，是供您維繫和另一半感情的得力助手。

## 網站功能

- 爬取景點文章功能
- 爬取當地天氣資訊功能
- 依客製化住宿選項爬取旅館功能
- 爬取禮品功能
- 文字雲功能

## 作品介紹

本產品為資科系期末專題作品，以 Python 做為開發語言，並且分為報告版與線上版。

- **報告版**用於撰寫報告，以作品完整、穩定為訴求，設計在個人電腦上運行（MacOS 環境），可參考 main branch 。
- **線上版**為展示用途，架設於 Heroku 伺服器，但目前仍在著手處理一些相容性所導致的 bugs ，可參考 heroku branch。[點我前往](https://our-private-life.herokuapp.com/)。

本產品所使用到的技術 / 工具：

- Flask
- Jinja
- Heroku
- Selenium
- BeautifulSoup
- WordCloud
- Jieba
- PIL
- Git
- Bootstrap

## 了解更多

若您對本作品感興趣，歡迎參訪以下連結了解更多：

- [體驗「Our Private Life」服務（開發中）](https://our-private-life.herokuapp.com/)
- [專題企劃書](https://docs.google.com/presentation/d/1HptT1haEJenpeMkw4398x-KB4QccmFVXwzZtzAsQVGs/edit?usp=sharing)

## 開發團隊

本專題由四人共同構想、貢獻：

- **莊天均**
    - 網站架構與視覺
    - Flask 環境搭建
    - 協助爬蟲技術
- **黃奕銘**
    - 爬取禮品資訊
- **陳奕君**
    - 網站架構發想
    - 爬取旅館資訊
    - 客製化訂房系統
- **記柔安**
    - 爬取天氣資訊
    - 爬取景點文章
