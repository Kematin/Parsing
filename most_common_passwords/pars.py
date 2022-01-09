import requests
from bs4 import BeautifulSoup
import json


url = 'https://en.wikipedia.org/wiki/Wikipedia:10,000_most_common_passwords'
headers = {
	'Accept': '*/*',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}

#Сохранение страницы в файл
def save_main_file(url):
	req = requests.get(url=url, headers=headers)
	src = req.text

	with open('index.html', 'w', encoding='utf-8') as file:
		file.write(src)


def main():
	with open('index.html', 'r') as file:
		src = file.read()

	soup = BeautifulSoup(src, 'lxml')

	tables = soup.find_all('div', {'class': 'div-col', 'style': 'column-width: 10em;'})

	first_table = tables[0].find_all('li')
	second_table = tables[1].find_all('li')

	save_passwords('top 100', first_table)
	save_passwords('top 101-10000', second_table)


def save_passwords(name, table):

	with open(f'{name}.txt', 'a') as file:
		for password in table:
			file.write(f'{password.text}\n')

	print(f'The {name} most frequent passwords were recorded')


main()
