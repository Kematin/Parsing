from bs4 import BeautifulSoup
import requests
from time import sleep
import os

class Parser:
    def __init__(self, url, headers, category_name):
        self.url = url
        self.headers = headers
        self.category_name = category_name
        self.default_url = 'https://rule34.world'

    
    def save_page(self, name, url):
        req = requests.get(url, headers=self.headers)
        scr = req.text

        with open(f'HTML/{name}.html', 'w', encoding="utf-8") as file:
            file.write(scr)
        print(f'{name}.html download')


    def open_page(self, name):
        with open(f'HTML/{name}.html', encoding="utf-8") as file:
            scr = file.read()
        soup = BeautifulSoup(scr, 'lxml')
        return soup

    
    def download_image(self, url, name, num):
        try:
            response = requests.get(url=url)

            with open(f'Photos/{self.category_name}/{name}.png', 'wb') as f:
                f.write(response.content)
            return f'Image #{num} was download'
        
        except Exception as e:
            return 'Error'

        finally:
            pass


    def __set_url(self, url):
        if len(url) > 40:
            return url
        else:
            return self.default_url + url


    def create_folder(self, foldername):
        try:
            os.mkdir(f'Photos/{foldername}')
            with open(f'HTML/{foldername}.html', 'r'):
                print('File already create')

        except FileExistsError as f:
            print('Folder already create')
        except FileNotFoundError:
            self.save_page(foldername, self.url) 

        finally:
            pass


    def main(self):
        soup = self.open_page(self.category_name)
        groups = soup.find_all('app-post-preview', class_='ng-star-inserted')
        hrefs = [self.default_url + group.find('a', class_='boxInner').get('href') for group in groups]

        for href in hrefs:
            req = requests.get(url=href, headers=self.headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')

            try:
                url = soup.find('img', class_='img shadow-base').get('src')
            except AttributeError:
                print('You try download video, not photo')

            image = self.__set_url(url)
            print(self.download_image(image, href[-1:-4:-1], hrefs.index(href) + 1))
            sleep(0.5)


def test():
    category = input('Category: ')
    pars.create_folder(category)


def start():
    headers = {
       	    'Accept': '*/*',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    }
    category = input('Category: ')
    url = 'https://rule34.world/' + category
    pars = Parser(url, headers, category)
    pars.main()


if __name__ == '__main__':
    start()
