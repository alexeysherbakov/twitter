from bs4 import BeautifulSoup
import requests
import smile

def smiles():
    smileface = smile.ace
    print(smileface)

def parser():
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
   } # Парсинг по User-Agent
   cookies = {'dataxd': 'alex'} # Парсинг по куки
   req = requests.get(url='http://127.0.0.1:5000/', headers=headers, cookies = cookies)
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