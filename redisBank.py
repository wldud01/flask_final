from flask import Flask, jsonify
import redis
#from dynamic import index
import json
from title import notice_check
#import requests

#app = Flask(__name__)
def redis_foodBank():
    # redis 연결
    redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)

    Announce_json = {}
    decode_list = []
    #for i,url in enumerate(notice_check()):
        #URL.append({'id':i,'url':url[i]})
    for i,content in enumerate(notice_check()):
        decode_dict = {}
        decode_dict['id'] = i #id
        decode_dict['src'] = content['src'].decode('utf-8') # 그 푸드뱅크 기부 사진
        decode_dict['title'] = content['title'].decode('utf-8') # 제목
        decode_dict['content'] = content['content'].decode('utf-8') # 내용
        decode_list.append(decode_dict)
    Announce_json['announce'] = decode_list

    jsonData = json.dumps(Announce_json, ensure_ascii=False).encode('utf-8')
    redis_client.set('Announce', jsonData)
    stored_data = redis_client.get('Announce')
    #decoded_data = json.loads(stored_data)
    print(stored_data)
    return jsonify(stored_data)
#redis_foodBank()