from bs4 import BeautifulSoup
import requests
from time import sleep

class Parser:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    
    def save_page(self, name, url):
        req = requests.get(url, headers=self.headers)
        scr = req.text

        with open(f'{name}.html', 'w', encoding="utf-8") as file:
            file.write(scr)
        print(f'{name}.html download')


    def open_page(self, name):
        with open(f'{name}.html', encoding="utf-8") as file:
	    scr = file.read()
        soup = BeautifulSoup(scr, 'lxml')
        return soup


    def create_folder(self):
        pass


    def main(self):
        # self.save_page('index', self.url) save main page


def start():
    headers = {
       	    'Accept': '*/*',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    }
    url = 'https://rule34.world/one-punch_man'
    pars = Parser(url, headers)
    pars.main()


if __name__ == '__main__':
    start()
