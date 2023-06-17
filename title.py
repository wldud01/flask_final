# 알림 뉴스 소식 인듯

import requests 
from bs4 import BeautifulSoup


# 홍보 소식 사진이랑 제목 가져오기는 완성
def notice_check():
    url = "https://www.foodbank1377.org/reference/promote.do" 
    res = requests.get(url) 
    res.raise_for_status() # 정상 200
    soup = BeautifulSoup(res.content, "html.parser")
    ul = soup.select_one('ul.grid') # 전체 영역에서 'a' 태그를 찾지 않고 인기 급상승 영역으로 범위 제한4
    a = ul.find_all('li')
    span = ul.find_all('em')
    print(span)  
    
    news_list =[]

    for i in range(0,len(a)):
        board_title = {}
        src = a[i].a['style']
        url = "https://www.foodbank1377.org"+src.split("'")[1]
        text_list=span[i].get_text().strip().split(' ')
        print(url)
        print(text_list)
        board_title['title'] = text_list[0].encode('utf-8')
        board_title['content'] = span[i].get_text().strip().encode('utf-8')
        board_title["src"]=url.encode('utf-8') # 사진
        news_list.append(board_title)
        print(news_list)
    return news_list
#"https://www.foodbank1377.org"+

#notice_check()