import random
import time
from dotenv import load_dotenv
from ParserData import STATUS_TYPES
from ConfigManager import ConfigManager
from DbManager import DbManager
import Scraper

load_dotenv()

config = ConfigManager()
db_manager = DbManager(config)


def add_data(book, processed_data):
    # insert book
    book_id = db_manager.insert_book(**vars(book))

    # insert authors
    authors_ids = []
    for name in book.authors:
        if name in processed_data['processed_authors'].keys():
            authors_ids.append(processed_data['processed_authors'][name])
            continue
        author_id = db_manager.insert_author(name=name)
        authors_ids.append(author_id)
        processed_data['processed_authors'][name] = author_id

    # insert book_authors
    for author_id in authors_ids:
        db_manager.insert_book_author(book_id, author_id)

    # insert genres
    if book.genre:
        if book.genre not in processed_data['processed_genres'].keys():
            genre_id = db_manager.insert_genre(book.genre)
            processed_data['processed_genres'][book.genre] = genre_id
        db_manager.insert_book_genre(book_id, processed_data['processed_genres'][book.genre])


    # insert users and reviews
    if len(book.reviews):
        for review in book.reviews:
            user = review.user
            user_id = db_manager.insert_user(**vars(review.user))
            db_manager.insert_review(book_id=book_id, user_id=user_id, review=review.text)
            db_manager.insert_rate(book_id=book_id, user_id=user_id, rate=random.randint(1, 10))

    return book_id, processed_data


if __name__ == '__main__':

    processed_data = {
        'processed_authors': {},
        'processed_book_isbn': [],
        'processed_series_names': [],
        'processed_genres': {}
    }

    series_id = 1

    counter = 0
    while len(processed_data['processed_book_isbn']) < config.max_books:
        book_id = random.randint(1, 19999999)

        url_part1 = 'https://www.bookvoed.ru/book?id='
        url_part2 = '#tdescription'
        url = url_part1 + str(book_id) + url_part2

        book = Scraper.get_book(url)
        counter += 1

        if book and book.isbn and not db_manager.is_book_add(book.isbn):
            book_id, processed_data = add_data(book, processed_data)

            # work with series
            if book.series and book.series not in processed_data['processed_series_names']:
                book_ids = Scraper.get_book_series(book.series_link)

                for scrap_book_id in book_ids:
                    url = url_part1 + str(scrap_book_id) + url_part2
                    book = Scraper.get_book(url)
                    counter += 1
                    if book and not db_manager.is_book_add(book.isbn):
                        book_id, processed_data = add_data(book, processed_data)
                        db_manager.insert_series(series_id, book_id, book.series)


                processed_data['processed_series_names'].append(book.series)
                time.sleep(random.randint(1, 3))
                series_id += 1

        time.sleep(random.randint(1, 3))

        if counter > 50:
            time.sleep(30)
            counter = 0


    sale_id = db_manager.insert_sale(5, None, None, 'Стандартная бессрочная скидка.')
    users_ids = db_manager.get_user_ids()
    book_ids = db_manager.get_book_ids()


    for idx, user_id in enumerate(users_ids):
        if idx % 5 != 0:
            continue
        order_id = db_manager.insert_order(user_id, 0.0, random.choice(STATUS_TYPES))

        books_in_order = random.randint(1, 5)
        for _ in range(books_in_order):
            book_id = random.choice(book_ids)
            price = db_manager.get_book_price(book_id)
            total_price = price - price * 0.05
            db_manager.insert_item_order(order_id, book_id, price, 1, sale_id, total_price)

    for idx, user_id in enumerate(users_ids):
        if idx % 35 != 0:
            continue
        order_id = db_manager.insert_order(user_id, 0.0, random.choice(STATUS_TYPES))

        books_in_order = random.randint(1, 3)
        for _ in range(books_in_order):
            book_id = random.choice(book_ids)
            price = db_manager.get_book_price(book_id)
            total_price = price - price * 0.05
            db_manager.insert_item_order(order_id, book_id, price, 1, sale_id, total_price)
