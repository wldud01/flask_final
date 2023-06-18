from flask import Flask,Response,jsonify
from numpy import object_
from soup import title_check
from preferItem import prefer
import redis
from flask_restful import Api, Resource
import pandas as pd

import json
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#app = Flask(__name__)
api = Api(app)
# flask의 화면을 띄우기
@app.route("/")
def nginx():
    app.logger.debug('debug')
    return 'hello! nginx'

@app.route('/tospring')
def hello():
    t=[]
    for i,title in enumerate(title_check()):
        t.append({'id':i,'title':title.decode('utf-8')})
    print(t)
    json_str = json.dumps(t,ensure_ascii=False)

    return  Response(json_str, content_type='application/json; charset=utf-8')

# 공지사항
@app.route('/Notices', methods=['GET'])
def get_titles():
    Title=[]
    title_dict = {}
    for i,title in enumerate(title_check()):
        Title.append({'id':i,'title':title.decode('utf-8')})
    print(Title)
    title_dict["Notices"] = Title

    return jsonify(title_dict)
    
@app.route('/Notices/<int:id>', methods=['GET'])
def get_title(id):
    Title=[]
    title_dict = {}
    for i,title in enumerate(title_check()):
        Title.append({'id':i,'title':title.decode('utf-8')})
    print(Title)
    title_dict["Notices"] = Title
    for item in title_dict():
        return item["Noices"][id]

    return jsonify({"message": " not found "})

# Announce page
@app.route('/Announces', methods=['GET'])
def get_Announces():
    decoded_data = {}
    redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)
    stored_data = redis_client.get('Announce')
    stored_data = stored_data.decode('utf-8')
    result = json.loads(stored_data)
    #decoded_data["ann"] = stored_data
    print(stored_data)
    return result
@app.route('/Announces/<int:id>', methods=['GET'])
def get_Announce(id):
    decoded_data = {}
    redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)
    stored_data = redis_client.get('Announce')
    stored_data = stored_data.decode('utf-8')
    result = json.loads(stored_data)
    for item in result:
        return result['announce'][id]
    return {"message": " not found "}

@app.route('/preferItem/<int:id>', methods=['GET'])
def preferDates(id):
    prefer_dict = {1:"라면류",2:"쌀",3:"밀가루",4:"고추장",5:"된장",6:"참기름",
               7:"가공햄류",8:"식용유",9:"통조림류",10:"설탕류",11:"간장류",12:"소면류",
               13:"김",14:"즉석밥",15:"샴푸",16:"치약",17:"비누"}
    prefer_itemsTotal = json.loads(prefer(id).encode('utf-8'))
    title__ = list(prefer_itemsTotal.keys())
    value = list(prefer_itemsTotal.values())
    preferItem_title = []
    preferItem_value = []
    prefer_top ={} 
    for i in range(0,len(title__)):
        print(prefer_dict[int(title__[i])])   # 부족한 물품
        preferItem_title.append(prefer_dict[int(title__[i])])
        preferItem_value.append(int(value[i]))
    prefer_top['prefer_title'] = preferItem_title
    prefer_top['prefer_value'] = preferItem_value
    return jsonify(prefer_top)

@app.route('/preferItem/top3/<int:id>', methods=['GET'])
def preferDate(id):
    prefer_dict = {1:"라면류",2:"쌀",3:"밀가루",4:"고추장",5:"된장",6:"참기름",
               7:"가공햄류",8:"식용유",9:"통조림류",10:"설탕류",11:"간장류",12:"소면류",
               13:"김",14:"즉석밥",15:"샴푸",16:"치약",17:"비누"}
    prefer_itemsTotal = json.loads(prefer(id).encode('utf-8'))
    preferItem_list = []
    prefer_top ={} 
    top3 = list(prefer_itemsTotal.keys())
    for i in range(0,3):
        print(prefer_dict[int(top3[i])])   # 부족한 물품
        preferItem_list.append(prefer_dict[int(top3[i])])
    prefer_top['top_three'] = preferItem_list
    return jsonify(prefer_top)




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port='5000', unix_sock='/home/jiyeong/flaskAPI/flaskAPI.sock' )