
if __name__ == '__main__':

    books = []

    urls = [
        'https://www.bookvoed.ru/book?id=11057475#tdescription',
        'https://www.bookvoed.ru/book?id=6709206#tdescription',
        'https://www.bookvoed.ru/book?id=13595759#tdescription',
        'https://www.bookvoed.ru/book?id=11579668#tdescription',
        'https://www.bookvoed.ru/book?id=6529250#tdescription'
    ]
    random.shuffle(urls)
    # while len(books) < 500:
    for url in urls:
        # id = random.randint(1, 19999999)
        # url = f'https://www.bookvoed.ru/book?id={id}#tdescription'

        # session = requests.Session()
        # cookies = {
        #     'cookie_name1': 'cookie_value1',
        #     'cookie_name2': 'cookie_value2',
        #     # Добавьте остальные куки
        # }
        # session.cookies.update(cookies)
        # headers = {
        #     'User-Agent': 'ваш юзер-агент',
        #     'Referer': 'URL реферера, если требуется',
        #     # Добавьте другие заголовки
        # }
        # session.headers.update(headers)


        try:
            response = requests.get(url, timeout=5)
            print(url, response.status_code)
            if response.status_code == 200:
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



                    for key, value in vars(book).items():
                        print(key, value)




                    # book.title = get_title(soup_html)
                    # book.title = get_title(soup_html)


        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            time.sleep(random.randint(0, 5))