# 공지사항 들어갔을 때 이미지 데이터

from soup import title_check
from io import BytesIO
from flask import jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from PIL import Image
import base64

#import requests

#app = Flask(__name__)
#redis_client = redis.Redis(host='localhost', port=6379, db=0) #없어질 것
#@app.route('/')
def index():
    # headless Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    # Chrome 드라이버 생성
    driver = webdriver.Chrome("/home/jiyeong/chromedriver.exe", options=chrome_options)

    # 웹 페이지 로드
    driver.get('https://www.foodbank1377.org/reference/notice.do')
    driver.implicitly_wait(3)
    page_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    page_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(page_width, page_height)
    # 버튼 클릭
    imglist = []
    for i in range(1,len(title_check())):
        imginfo= {}
        button = driver.find_element(By.XPATH,r'//*[@id="main"]/div/div[2]/table/tbody/tr[{}]/td[3]/a'.format(i))
        button.click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select_one('div.bd-contents')
        img = data.find('img')

        
        #print(a)
        if img is not None:
           
            src = img['src']
            imginfo['id'] = i
            imginfo['url']= src
        else:
            element = driver.find_element(By.XPATH,r'//*[@id="main"]/div/div[2]/div[2]/div[2]')
            location = element.location
            size = element.size
            print('Element location:', location)
            print('Element size:', size)

            screenshot = driver.get_screenshot_as_png()
            x = location['x']
            y = location['y']
            width = size['width']
            height = size['height']
            image = Image.open(BytesIO(screenshot)).crop((x, y, x + width, y + height))
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            

            # imglist에 값을 전부 저장 
            image.save(f"image{i}.png")
            imginfo['id'] = i 
            imginfo['title'] = title_check()[i].decode('utf-8') 
            imginfo['url'] = f"https://localhost:5000/image{i}.jpg"
            imginfo['data'] = img_str
        imglist.append(imginfo)
        driver.find_element(By.XPATH,r'//*[@id="main"]/div/div[2]/div[3]/button').click()
            

        # iframe 내부로 이동
        #driver.switch_to.frame('iframe-id')

        # iframe 내부의 HTML 코드 가져오기
        #html = driver.page_source
        #soup = BeautifulSoup(html, 'html.parser')

        # 데이터 추출
        #data = soup.select_one('div.bd-contents').get_text().strip()
        #print(data)
        

    # Chrome 드라이버 종료
    driver.quit()
    
    print(imglist) #전체 값을 가지고 있는 값 

    # redis 설정 data변수에 값을 다 넣음
    #redis_client.set('data', json.dumps(imglist))
    #stored_data = redis_client.get('data')
    #decoded_data = json.loads(stored_data)

    
    # 추출한 데이터를 JSON 형태로 반환
    return imglist

#if __name__ == '__main__':
 #   app.run(debug=True)