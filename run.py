import random
from dotenv import load_dotenv

from ConfigManager import ConfigManager
from DbManager import DbManager
import Scraper

load_dotenv()

config = ConfigManager()
db_manager = DbManager(config)

db_manager.create_tables()

if __name__ == '__main__':
    books = []
    urls = [
        'https://www.bookvoed.ru/book?id=13617607#tdescription',
        'https://www.bookvoed.ru/book?id=13635069#tdescription',
        'https://www.bookvoed.ru/book?id=13578048#tdescription',
        'https://www.bookvoed.ru/book?id=13542521#tdescription',
        'https://www.bookvoed.ru/book?id=376402#tdescription'
    ]
    random.shuffle(urls)

    # while len(books) < 500:
    for url in urls:

        # id = random.randint(1, 19999999)
        # url = f'https://www.bookvoed.ru/book?id={id}#tdescription'

        book = Scraper.get_book(url)

        if book:
            db_manager.add_book(**vars(book))

            if len(book.reviews):
                for review in book.reviews:
                    user = review.user[0]
                    user_id = db_manager.add_user(**vars(user))
                    print(user_id)


