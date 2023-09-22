import psycopg2
from ConfigManager import ConfigManager



class DbManager:
    def __init__(self, config: ConfigManager):
        self.ConfigManager = config

        self.db_name = config.db_name
        self.db_user = config.db_user
        self.db_password = config.db_password
        self.db_host = config.db_host
        self.db_port = config.db_port
        self.connection = self.get_connection()

        if self.connection is None:
            print('Error! Can not connect to db.')
            exit()

    def get_connection(self):
        try:
            conn = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            return conn
        except Exception as e:
            print(e)

    def execute(self, query, values=None):

        result = None

        try:
            cursor = self.connection.cursor()

            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)

            self.connection.commit()

            result = cursor.fetchall()

        except Exception as e:
            if "no results to fetch" in str(e):
                pass
            else:
                self.connection.rollback()
                print(e)

        return result

    def execute_file(self, file_path):
        with open(file_path, 'r') as sql_file:
            sql_queries = sql_file.read().split(";")
            for query in sql_queries:
                if len(query.strip()):
                    self.execute(query)

    def insert_book(self, isbn=None, title=None, description=None, price=None,
                    rating=None, publ_year=None, publisher=None, num_pages=None,
                    cover_type=None, height=None, width=None, thickness=None,
                    weight=None, **kwargs):
        query = '''
            INSERT INTO BOOKS (
                ISBN, TITLE, DESCRIPTION, PRICE, RATING, PUBL_YEAR, PUBLISHER,
                NUM_PAGES, COVER_TYPE, HEIGHT, WIDTH, THICKNESS, WEIGHT
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            RETURNING BOOK_ID;
        '''
        values = (isbn, title, description, price, rating, publ_year, publisher,
                  num_pages, cover_type, height, width, thickness, weight)
        response = self.execute(query, values)

        if response:
            return response[0][0]
        return None

    def insert_user(self, name=None, email=None, password=None, phone_num=None,
                    role_name=None, birthday=None, active_status=None, **kwargs):
        query = '''
            INSERT INTO USERS (
                NAME, EMAIL, PASSWORD, PHONE_NUM, ROLE_ID, BIRTHDAY, ACTIVE_STATUS
            )
            VALUES (
                %s, %s, %s, %s, (SELECT ROLE_ID FROM ROLES WHERE ROLE_NAME = %s), %s, %s
            )
            RETURNING USER_ID;
        '''
        values = (name, email, password, phone_num, role_name, birthday, active_status)
        response = self.execute(query, values)

        if response:
            return response[0][0]
        return None

    def insert_author(self, name=None, birthday=None, description=None, **kwargs):
        query = '''
            INSERT INTO AUTHORS (
                AUTHOR_NAME, BIRTHDAY, DESCRIPTION
            )
            VALUES (
                %s, %s, %s
            )
            RETURNING AUTHOR_ID;
        '''
        values = (name, birthday, description)
        response = self.execute(query, values)

        if response:
            return response[0][0]
        return None

    def insert_book_author(self, book_id=None, author_id=None):
        query = '''
            INSERT INTO BOOK_AUTHORS (
                BOOK_ID, AUTHOR_ID
            )
            VALUES (
                %s, %s
            )
        '''
        values = (book_id, author_id)
        self.execute(query, values)

    def insert_review(self, book_id=None, user_id=None, review=None):
        query = '''
            INSERT INTO REVIEWS (
                BOOK_ID, USER_ID, REVIEW
            )
            VALUES (
                %s, %s, %s
            )
        '''
        values = (book_id, user_id, review)
        self.execute(query, values)

    def insert_rate(self, book_id=None, user_id=None, rate=None):
        query = '''
            INSERT INTO RATES (
                BOOK_ID, USER_ID, RATE
            )
            VALUES (
                %s, %s, %s
            )
        '''
        values = (book_id, user_id, rate)
        self.execute(query, values)

    def insert_series(self, series_id=None, book_id=None, series_name=None):
        query = '''
            INSERT INTO BOOKS_SERIES (
                SERIES_ID, BOOK_ID, SERIES_NAME
            )
            VALUES (
                %s, %s, %s
            )
        '''
        values = (series_id, book_id, series_name)
        self.execute(query, values)

    def is_book_add(self, book_isbn=None):
        query = '''
            SELECT BOOK_ID FROM BOOKS WHERE ISBN = %s
        '''
        values = (book_isbn,)
        res = self.execute(query, values)
        if len(res):
            return True
        return False

    def insert_genre(self, genre=None, description=None):
        query = '''
            INSERT INTO GENRE_TAGS (
                GENRE_TAG_NAME, DESCRIPTION
            )
            VALUES (
                %s, %s
            )
            RETURNING GENRE_TAG_ID;
        '''
        values = (genre, description)
        response = self.execute(query, values)
        if response:
            return response[0][0]
        return None

    def insert_book_genre(self, book_id=None, genre_id=None):
        query = '''
            INSERT INTO BOOK_GENRE_TAGS (
                BOOK_ID, GENRE_TAG_ID
            )
            VALUES (
                %s, %s
            )
        '''
        values = (book_id, genre_id)
        self.execute(query, values)

    def insert_sale(self, percent=None, start_period=None, stop_period=None, description=None):
        query = '''
            INSERT INTO SALES (
                SALE_PERCENT, START_PERIOD, STOP_PERIOD, DESCRIPTION
            )
            VALUES (
                %s, %s, %s, %s
            )
            RETURNING SALE_ID;
        '''
        values = (percent, start_period, stop_period, description)
        response = self.execute(query, values)
        if response:
            return response[0][0]
        return None


    def get_user_ids(self):
        query = '''
            SELECT USER_ID FROM USERS
        '''
        res = self.execute(query)
        if len(res):
            return [i[0] for i in res]
        return []

    def get_book_ids(self):
        query = '''
            SELECT BOOK_ID FROM BOOKS
        '''
        res = self.execute(query)
        if len(res):
            return [i[0] for i in res]
        return []

    def insert_order(self, user_id=None, total_price=None, status=None):
        query = '''
            INSERT INTO ORDERS (
                USER_ID, TOTAL_PRICE, STATUS
            )
            VALUES (
                %s, %s, %s
            )
            RETURNING ORDER_ID;
        '''
        values = (user_id, total_price, status)
        response = self.execute(query, values)
        if response:
            return response[0][0]
        return None

    def get_book_price(self, book_id):
        query = f'SELECT PRICE FROM BOOKS WHERE BOOK_ID = {book_id}'
        response = self.execute(query)
        if len(response):
            return response[0][0]
        return None

    def insert_item_order(self, order_id=None, book_id=None, price=None, quantity=None, sale_id=None, total_price=None):
        query = '''
            INSERT INTO ORDER_ITEMS (
                ORDER_ID, BOOK_ID, BOOK_PRICE, QUANTITY, SALE_ID, TOTAL_ITEM_PRICE
            )
            VALUES (
                %s, %s, %s, %s, %s, %s
            )
            RETURNING ORDER_ID;
        '''
        values = (order_id, book_id, price, quantity, sale_id, total_price)
        self.execute(query, values)
