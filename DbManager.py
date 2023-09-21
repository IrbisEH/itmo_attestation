import psycopg2
from ConfigManager import ConfigManager



class DbManager:
    def __init__(self, config: ConfigManager):
        self.ConfigManager = config

        self.create_tables_file = config.create_tables_file

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
        try:
            cursor = self.connection.cursor()
            if values:
                res = cursor.execute(query, values)
            else:
                res = cursor.execute(query)
            self.connection.commit()

            if res:
                return res

        except Exception as e:
            self.connection.rollback()
            print(e)

    def create_tables(self):
        with open(self.create_tables_file, 'r') as sql_file:
            sql_queries = sql_file.read().split(";")
            for query in sql_queries:
                if len(query.strip()):
                    self.execute(query)

    def add_book(self, isbn=None, title=None, description=None, price=None,
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
        '''
        values = (isbn, title, description, price, rating, publ_year, publisher,
                  num_pages, cover_type, height, width, thickness, weight)
        self.execute(query, values)

    def add_user(self, name=None, email=None, password=None, phone_num=None,
                 role_name=None, birthday=None, active_status=None, **kwargs):
        query = '''
            INSERT INTO USERS (
                NAME, EMAIL, PASSWORD, PHONE_NUM, ROLE_ID, BIRTHDAY, ACTIVE_STATUS
            )
            VALUES (
                %s, %s, %s, %s, (SELECT ID FROM ROLES WHERE ROLE_NAME = %s), %s, %s, %s, %s, %s, %s, %s, %s
            )
            RETURNING USER_ID;
        '''
        values = (name, email, password, phone_num, role_name, birthday, active_status)
        user_id = self.execute(query, values)
        return user_id
