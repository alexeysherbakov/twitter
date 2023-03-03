from bs4 import BeautifulSoup
import requests
import smile
from fake_useragent import UserAgent

ua = UserAgent()

def smiles():
    smileface = smile.ace
    # print(smileface)

def parser():
   
   with open('proxy.txt') as file:
       proxies = ''.join(file.readlines()).strip().split('\n')

   headers = {
       'User-Agent': ua.random
   } # Парсинг по User-Agent

   req = None
   data = []
   for prox in proxies:
    proxies = {
        'http': f'http://{prox}',
        'https': f'http://{prox}'
    }
   cookies = {'dataxd': 'alex'} # Парсинг по куки
   try:
    req = requests.get(url='http://127.0.0.1:5000/', headers=headers, proxies=proxies, cookies=cookies, timeout=2)
    print(req)
    print(req.request.text)
    print(req.request.headers)
    print('Hello')
    #    print(req.request.headers)
   except:
      print('Bad proxy...') 

   if req is not None:
      soup = BeautifulSoup(req.content, 'lxml')   
      data = soup.find_all('p', class_='listing')

   for i in data:
       links = i.find('a').get('href')
       print((i.text.replace('ссылка', '').replace(',',''))+f'http://127.0.0.1:5000{links}')

def main():
    parser()
    smiles()

if __name__ == '__main__':
    main()