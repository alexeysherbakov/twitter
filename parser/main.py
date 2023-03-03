from bs4 import BeautifulSoup
import requests
import smile
from fake_useragent import UserAgent

ua = UserAgent()

def smiles():
    smileface = smile.ace
    # print(smileface)

def parser():
   headers = {
       'User-Agent': ua.random
   } # Парсинг по User-Agent
   proxies = {
       'https': 'http://185.162.231.12:80'
   } # Парсинг по прокси
   cookies = {'dataxd': 'alex'} # Парсинг по куки
   req = requests.get(url='http://127.0.0.1:5000/', headers=headers, cookies = cookies, proxies=proxies)
   print(req.request.headers)
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