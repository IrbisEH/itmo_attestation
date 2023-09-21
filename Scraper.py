import requests
import random
import string
from datetime import datetime, timedelta
import re
import traceback
from bs4 import BeautifulSoup

from ParserData import KEY_TRANSFORM, COVER_TYPES, PUBLISHERS, SIZES, GENRES, EMAIL_DOMAINS


class User:
    def __init__(self, name=None):
        self.name = name
        self.email = self.generate_email()
        self.password = self.generate_password()
        self.phone_num = self.generate_phone_num()
        self.birthday = self.generate_birthday()
        self.role_name = 'customer'
        self.active_status = True

    def generate_email(self):
        username_length = random.randint(5, 10)
        username = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(username_length))
        domain = random.choice(EMAIL_DOMAINS)
        email = f"{username}@{domain}"
        return email

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(10))
        return password

    def generate_phone_num(self):
        num = random.randint(1111111111, 9999999999)
        return f'8{num}'

    def generate_birthday(self):
        start_date = datetime(1950, 1, 1)
        end_date = datetime(2010, 12, 31)
        return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'phone_num': self.phone_num,
            'birthday': self.birthday,
            'role_name': self.role_name,
            'active_status': self.active_status
        }


class Review:
    def __init__(self, user=None, review_text=None):
        self.user = user,
        self.text = review_text


class Book:
    def __init__(self):
        self.isbn = None
        self.title = None
        self.authors = None
        self.price = None
        self.description = None
        self.publ_year = None
        self.publisher = None
        self.num_pages = None
        self.cover_type = None
        self.height = None
        self.width = None
        self.thickness = None
        self.weight = None
        self.genre = None
        self.size = None
        self.series = None
        self.series_link = None
        self.reviews = []

    def transform(self):
        if self.authors:
            self.authors = self.authors.split(',')
            self.authors = [i.strip() for i in self.authors]

    def get_random_values(self):
        if self.price is None:
            self.price = random.randint(200, 600)
        if self.publ_year is None:
            self.publ_year = random.randint(2000, 2023)
        if self.publisher is None:
            self.publisher = random.choice(PUBLISHERS)
        if self.num_pages is None:
            self.num_pages = random.randint(200, 1500)
        if self.cover_type is None:
            self.cover_type = random.choice(COVER_TYPES)
        if self.size is None:
            format = random.choice(list(SIZES.keys()))
            self.height = SIZES[format]['height']
            self.width = SIZES[format]['width']
            self.thickness = random.randint(15, 35)
        if self.weight is None:
            self.weight = random.randint(150, 450)


def get_book(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            raise Exception(f'{url} code: {response.status_code}')

        soup_html = BeautifulSoup(response.text, 'html.parser')

        if is_book_page(soup_html):
            book = Book()
            book.title = get_title(soup_html)
            book_info = get_book_info(soup_html)
            for key, value in book_info.items():
                setattr(book, key, value)
            book.description = get_description(soup_html)
            book.series, book.series_link = get_series_info(soup_html)
            book.price = get_price(soup_html)
            book.reviews = get_reviews(soup_html)

            book.transform()
            book.get_random_values()

            return book


    except Exception as e:
        print(e)
        traceback.print_exc()


def is_book_page(soup_html):
    cat_element = soup_html.find('div', class_='xI')
    if cat_element:
        element = cat_element.find('span', itemprop='name', text='Книги')
        if element is not None and element.get_text() == 'Книги':
            return True
    return False


def get_title(soup_html):
    title = soup_html.find('h1', itemprop='name')
    if title is not None:
        return title.get_text()
    return None


def get_book_info(soup_html):
    result = {}
    info_table = soup_html.find('table', class_='XE')

    if info_table is None:
        return None

    rows = info_table.find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        if len(columns) == 2:
            key = columns[0].text.strip()
            value = columns[1].text.strip()
            if key in KEY_TRANSFORM.keys():
                result[KEY_TRANSFORM[key]] = value

    return result


def get_description(soup_html):
    element = soup_html.find('div', class_='oH')
    if element:
        return element.text.strip()
    return None


def get_series_info(soup_html):
    series_element = soup_html.find('td', text='Серия')
    if series_element:
        series_link = series_element.find_next('a')
        if series_link:
            series_url = series_link.get('href')
            series_name = series_link.text.strip()
            return series_name, series_url
    return None, None


def get_price(soup_html):
    html_element = soup_html.find('div', class_='SG')
    if html_element:
        price = html_element.get_text().strip()
        price = ''.join(filter(str.isdigit, price))
        return int(price)
    return None


def get_reviews(soup_html):
    reviews = []
    html_elements = soup_html.find_all('div', class_='rn')
    for el in html_elements:
        user_el = el.find('a', class_='Ln')
        username = user_el.get_text().strip() if user_el else None
        review_el = el.find('div', class_='go')
        review_text = review_el.get_text().strip() if review_el else None
        if username is not None and review_text is not None:
            user = User(username)
            review = Review(user, review_text)
            reviews.append(review)
    return reviews
