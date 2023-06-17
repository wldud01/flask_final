import requests
import json
import pandas as pd

#requestData = requests.get('https://openapi.foodbank1377.org/foodBankInfoService/getPreferInfo')

prefer_dict = {1:"라면류",2:"쌀",3:"밀가루",4:"고추장",5:"된장",6:"참기름",
               7:"가공햄류",8:"식용유",9:"통조림류",10:"설탕류",11:"간장류",12:"소면류",
               13:"김",14:"즉석밥",15:"샴푸",16:"치약",17:"비누"}
def prefer(id):
    if id < 10:
        id = '0'+ str(id)
    else:
        id = str(id)
    print(id)
    url = 'http://apis.data.go.kr/B460014/foodBankInfoService2/getPreferInfo'
    params ={'serviceKey' : 'ewIlnjfA4CehDBh4jEHga0/LDYGy0pEvETEQbKXyhyV4vV0gaIlpQgfzvfCQWUaIBY5BhPk86HpeKtA131eJBw==', 
            'numOfRows' : '1','pageNo':'1' ,'dataType':'JSON', 'areaCd' : id}

    response = requests.get(url, params=params)
    data = json.loads(response.text)
    totalCount = data['response']['body']['totalCount']
    params ={'serviceKey' : 'ewIlnjfA4CehDBh4jEHga0/LDYGy0pEvETEQbKXyhyV4vV0gaIlpQgfzvfCQWUaIBY5BhPk86HpeKtA131eJBw==', 
            'numOfRows' : f'{totalCount}','pageNo':'1' ,'dataType':'JSON', 'areaCd' : id}
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    #print(totalCount)
    # pandas import
    
    result = data['response']['body']['items']
    # Dataframe으로 만들기
    df = pd.DataFrame(result)
    forPrefer = df[['areaCd','preferCnttgClscd','holdQy']]
    forPrefer = forPrefer.astype({'holdQy': int , 'preferCnttgClscd': int})
    prefer_total = forPrefer.groupby('preferCnttgClscd')['holdQy'].sum()
    prefer_total = prefer_total.sort_values()
    preferItem_total_json = prefer_total.to_json(orient = 'columns')
    preferItem_list = []
    shortage = list(prefer_total.head(3).keys()) 
    for i in shortage:
        print(prefer_dict[i])   # 부족한 물품
        preferItem_list.append(prefer_dict[i])
    #preferItem_total_json['topThree']  = preferItem_list
    print(forPrefer['preferCnttgClscd'].value_counts())
    return  preferItem_total_json 
#print(prefer(1))