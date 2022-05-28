import requests
import json 

response = requests.get("http://api.open-notify.org/iss-now.json")
issPositionText = response.text

print()
print('b) API資料抓回來後，直接顯示其內容。目前內容仍存在記憶體變數中，未存檔。')
print('issPositionText:')
print(issPositionText)
print()

issPositionJsonDoc = json.loads(issPositionText)
print('------------')
print('c) 藉json模組的method將JSON字串decode為Python內設資料型態(dict/list等)。')
print('issPositionJsonDoc:')
print(issPositionJsonDoc)
print('type(issPositionJsonDoc): ' + str(type(issPositionJsonDoc)))
print()

fileName = 'D:/Python/ExcelReadWrite/issPosition.json'
jsonFile = open(fileName, 'w', encoding='utf-8')

json.dump(issPositionJsonDoc, jsonFile, ensure_ascii=False)
jsonFile.flush()
jsonFile.close()

jsonFile = open(fileName, 'r', encoding='utf-8-sig')