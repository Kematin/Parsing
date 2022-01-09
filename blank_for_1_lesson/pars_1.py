from bs4 import BeautifulSoup
import re

#Открытие страницы
file = 'E:\\Programming\\Python\\Парсинг, selenium\\Парсинг\\blank_for_1_lesson\\index.html'
with open(file) as file:
    scr = file.read()

#Преобразования класса со значениями страницы и вида парсера
soup = BeautifulSoup(scr, 'lxml')

'''
Элемент по тегу и вывод текста из этого элемента
title = soup.title
print(title)
print(title.text)
print(title.string)
'''

#.find(), .find_all()
def finds():
    first_h1 = soup.find('h1')

    all_h1 = soup.find_all('h1')
    print(first_h1)
    print(all_h1[0], all_h1[1])

    #ИЛИ

    for item in all_h1:
        print(item)


def find_class():
    #Поиск имени по классу
    class_name = soup.find('div', class_='user__name')
    print(class_name.text.strip())

    #Углублённый поиск имени по классу и по тегу
    more = soup.find('div', class_='user__name').find('span')
    print(more)

    #Поиск по словарю (удобно для более жёсткого отбора т.к. там можно указать несколько атрибутов)
    devv = soup.find('div', {'class' : 'user__name'}).find('span')
    print(devv)
   


def all_info():
    all_spans_from_user_info = soup.find('div', class_ = 'user__info').find_all('span')
    for span in all_spans_from_user_info:
        print(span.text)

    social_link = soup.find('div', class_ = 'social__networks').find('ul').find_all('a')
    print(social_link)


    all_a = soup.find_all('a')
    for item in all_a:
        item_url = item.get('href')
        print(f'{item_url} ---------- {item.text}')


#find_parent(), find_parents()


def parents():
    #Забираем код до первого родителя
    #user__post__info
    post_div = soup.find('div', class_ = 'post__text').find_parent()
    print(post_div)



#.next_element ----- .previous_element ------ .find_next()

def elements():
    next_el = soup.find(class_ = 'post__title').next_element.next_element.text
    #next_el = soup.find(class_ = 'post__title').find_next().text

    prev_el = soup.find(class_ = 'post__title').previous_element.previous_element.text.strip()

    print(f'Предыдущий элемент ------- {prev_el}\nСледующий элемент ---------- {next_el}')



#Методы .find_next_sibling() и .find_previous_sibling()
#Ищет предыдущий и следующий элемент внутри искомого тега

def sibling():
    next_sib = soup.find(class_ = 'post__title').find_next_sibling() 
    prev_sib = soup.find(class_ = 'post__title').find_previous_sibling()
    print(f'Предыдущий элемент --------- {prev_sib.text}\nСледующий элемент ----------- {next_sib.text}')
    

def training():
    links = soup.find('div', class_='some_link').find_all('a')
    for item in links:
        link = item.get('href')
        data_atr = item.get('data-atr')

        #link = item['href']
        #data_atr = item['data-atr']

        print(f'{link} : {data_atr} : {item.text}')


def find_by_text():
    #Выведет None т.к. текст не полный
    element = soup.find('h3', text='Wi-Fi')
    print(element)

    #Функция модуля re решает эту проблему
    element = soup.find('h3', text=re.compile('Wi-Fi'))
    print(element)

    #Но возникает проблема регистра при переборе всех тегов
    elements = soup.find_all('h3', text=re.compile('[Ww]i-[Ff]i'))
    for element in elements:
        print(element.string)


