import requests
from bs4 import BeautifulSoup
import json
import lxml
import selenium
from time import sleep
from math import ceil

url = 'https://news.ycombinator.com/news'
headers = {
	'Accept': '*/*',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}

def get_index(url):
	req = requests.get(url=url, headers=headers)
	src = req.text

	with open('index.html', 'w', encoding='utf-8') as file:
		file.write(src)


def main(end_point, start_point):
	with open('index.html', 'r', encoding='utf-8') as file:
		src = file.read()

	soup = BeautifulSoup(src, 'lxml')
	items = soup.find('table', class_='itemlist').find_all('tr', class_='athing')[start_point-1:]

	#for _ in range(ceil(end_point / 30)):
	get_tables(items, end_point)


def get_tables(table, end_point):
	for item in table:
		rank = item.find('span', class_='rank').text[:-1]

		data = item.find_all('td', class_='title')[1].find('a')

		tittle = data.text
		href = data.get('href')

		save_to_json(tittle, href, rank)
		
		sleep(2)
		print(f'The {tittle}\nwas recorded in json file')
		if int(rank) == end_point: break
	


def save_to_json(tittle, url, rank):
	groups_dict = {
		'tittle': tittle,
		'href': url,
		'number': rank
	}

	replace = [':', ',', '.', '?', '!', ';', ' ', '(', ')']
	for i in replace:
		if i in tittle:
			tittle = tittle.replace(i, '_')

	with open(f'data/{rank}__{tittle}.json', 'w', encoding='utf-8') as file:
		json.dump(groups_dict, file, indent=4, ensure_ascii=False)


def get_info_from_user():
	how_much = input('How much news do you want to stockpile\n')
	start_with = input('which news you want to start with (number).\n')

	while not how_much.isdigit():
		how_much = input('You entered an invalid value (how much)\n')

	while not start_with.isdigit():
		start_with = input('You entered an invalid value (start with)\n')

	return int(how_much), int(start_with)


if __name__ == '__main__':
	how_much, start_with = get_info_from_user()
	main(how_much, start_with)

