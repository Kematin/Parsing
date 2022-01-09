from bs4 import BeautifulSoup
import requests
import json
import csv
from time import sleep
from random import randrange

href = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
headers = {
	'Accept': '*/*',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}

#Импорт главной страницы
def create_file(url, head):
	req = requests.get(url, headers=head)
	scr = req.text


	with open('index.html', 'w', encoding="utf-8") as file:
		file.write(scr)



#Открытие страницы 
with open('index.html', encoding="utf-8") as file:
	scr = file.read()
soup = BeautifulSoup(scr, 'lxml')


#Перебор ссылок и название еды и сохранения их в словарь
def create_dict():
	all_groups_food = soup.find_all('a', class_='mzr-tc-group-item-href')
	all_groups_dict = {}
	for item in all_groups_food:
		url = 'https://health-diet.ru' + item.get('href')
		all_groups_dict[item.text] = url



#Сохранение словаря в json файл
def save_in_json():
	with open('for_second_lesson.json', 'w', encoding="utf-8") as file:
		json.dump(all_groups_dict, file, indent=4, ensure_ascii=False)




with open('for_second_lesson.json', encoding="utf-8") as file:
	all_groups = json.load(file)


replace = [',' , ' ', '-', '`']
def save_all_files():
	count = 0
	for name, href in all_groups.items():
		#Замена некоторых символов на _
		for i in replace:
			if i in name:
				name = name.replace(i, "_")

		req = requests.get(href, headers=headers)
		src = req.text

		#Сохранение всех страниц в файлы
		with open(f'data_2_lesson/{count}__{name}.html', 'w', encoding="utf-8") as file:
			file.write(src)
		count += 1
		print(f'Продукт {name} был успешно скачан')
		sleep(2)


def read_files():
	count = 0

	itiration = int(len(all_groups)) - 1
	print(f'Всего итераций {itiration}')

	for name, href in all_groups.items():
		#Замена некоторых символов на _
		for i in replace:
			if i in name:
				name = name.replace(i, "_")

		req = requests.get(href, headers=headers)
		src = req.text

		#Чтение страниц
		with open(f'data_2_lesson/{count}__{name}.html', encoding="utf-8") as file:
			src = file.read()

		soup = BeautifulSoup(src, 'lxml')

		#Проверка на наличие страницы
		alert = soup.find('div', class_='uk-alert uk-alert-danger uk-h1 uk-text-center mzr-block mzr-grid-3-column-margin-top')
		if alert is not None:
			count += 1
			continue


		#Импорт таблицы и заголовков
		table = soup.find('div', class_='uk-overflow-container').find('tr').find_all('th')
		save_to_csv(count, name, table, 'w')


		#Сбор данных о блюде
		product_info = []
		product_data = soup.find('div', class_='uk-overflow-container').find('tbody').find_all('tr')
		for item in product_data:
			data = item.find_all('td')

			tittle = data[0].text.strip()
			callories = data[1].text.strip()
			proteins = data[2].text.strip()
			fats = data[3].text.strip()
			carbohydrates = data[4].text.strip()


			product_info.append(
					{
						'tittle': tittle,
						'callories': callories,
						'proteins': proteins,
						'fats': fats,
						'carbohydrates': carbohydrates
					}
				)

			save_to_csv(count, name, data, 'a')


		with open(f'json_2_lesson/{count}__{name}.json', 'w', encoding='utf-8') as file:
			json.dump(product_info, file, indent=4, ensure_ascii=False)
		

		count += 1
		print(f'# Итерация: {count}. {name} был успешно обработон')
		itiration -= 1

		if itiration == 0:
			print('Конец работы')
			break

		print(f'Осталось {itiration} итераций')
		sleep(randrange(2, 4))


def save_to_csv(count, name, table, flag):
	product = table[0].text.strip()
	callories = table[1].text
	proteins = table[2].text
	fats = table[3].text
	carbohydrates = table[4].text

	with open(f'info_for_2_lesson/{count}__{name}.csv', flag, encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(
				(
					product,
					callories,
					proteins,
					fats,
					carbohydrates
				)
			)

save_all_files()
read_files()