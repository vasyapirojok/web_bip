from sqlalchemy import create_engine, Column, String, select, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2
import json


Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'
    email = Column(String, primary_key=True)
    password = Column(String)
    AES_key = Column(String)
    code = Column(String)


class database:
    def __init__(self, path: str = './database.db') -> None:
        engine = create_engine(f'sqlite:///{path}', echo=False)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)

    def add_user(self, email: str, password: str, code: str, key: int):
        session = self.Session()
        
        try:
            session.add(Users(email= email, password = str(hash(password)), AES_key = str(key), code=code))
            session.commit()
            session.close()
        except Exception as e:
            print(e)
            return False
        else:
            return True
        
    def check_creds(self, email, password):
        session = self.Session()
        result = session.execute(select(Users).filter_by(email = email)).first()
        session.close()
        
        if result != None and result[0].password == hash(password):
            return True
        else:
            return False
        
        
    def get_code(self, email):
        session = self.Session()
        result = session.execute(select(Users).filter_by(email = email)).first()
        session.close()
        return result[0].code


    def get_key(self, email):
        session = self.Session()
        result = session.execute(select(Users).filter_by(email = email)).first()
        # user = result.fetchone()
        session.close()
        return int(result[0].AES_key).to_bytes(32, 'little')

    def get_password(self, email):
        session = self.Session()
        result = session.execute(select(Users).filter_by(email = email)).first()
        session.close()
        return result[0].password         
    # def get_email(self, email):
    #     session = self.Session()
    #     result = session.execute(select(Users).where(Users.email == email))
    #     user = result.fetchone()
    #     if user!= None:
    #         return user.email
    #     else:
    #         return None
        
    def check_email(self, email):
        session = self.Session()
        result = session.execute(select(Users).filter_by(email = email)).first()
        session.close()
        if result == None:
            return True
        else:
            return False
        
    def set_code(self, email: str, code: str):
        session = self.Session()
        result = session.execute(select(Users).filter_by(email = email)).first()
        result[0].code = code
        session.commit()
        session.close()

class DB:
    def __init__(self):
        # conn = psycopg2.connect(
        #     database="postgres", user='postgres', password='1111', host='127.0.0.1', port= '5432'
        # )
        # cursor = conn.cursor()
        # cursor.execute("""SELECT 'CREATE DATABASE bip_db' 
        #                 WHERE NOT EXISTS 
        #                 (SELECT FROM pg_database WHERE datname = 'bip_db')""")
        # cursor.close()
        # conn.close()
        # self.__connect()

        self.query("CREATE TABLE IF NOT EXISTS credentials (email TEXT, password TEXT, salt TEXT, code TEXT, csrf TEXT)")
        self.query("CREATE TABLE IF NOT EXISTS catalog (shop TEXT, product JSON, id SERIAL)")

    def query(self, query: str):
        with psycopg2.connect(
            database="bip_db", user='postgres', password='1111', host='127.0.0.1', port= '5432'
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                try:
                    return [x for x in cursor]
                except:
                    return None

    def add_user(self, email: str, salt: str):
        self.query(f"INSERT INTO credentials (email, salt) VALUES('{email}', '{salt}')")

    def get_password(self, email: str):
        cursor_res = self.query(f"SELECT password FROM credentials WHERE email='{email}'")
        if cursor_res:    
            return cursor_res[0][0]
        return None

    def get_user(self, email: str):
        cursor_res = self.query(f"SELECT email, password FROM credentials WHERE email='{email}'")
        if not cursor_res:    
            return None
        return {"username": cursor_res[0][0], "hashed_password": cursor_res[0][0], "disabled": False}

    def check_creds(self, email: str, password: str):
        cursor_res = self.query(f"SELECT password FROM credentials WHERE email='{email}'")
        if cursor_res:
            return cursor_res[0][0] == password
        return None
    
    def check_email_exists(self, email: str):
        cursor_res = self.query(f"SELECT email FROM credentials WHERE email='{email}'")
        if not cursor_res:
            return False
        return True
    
    def set_password(self, email: str, password: str):
        self.query(f"UPDATE credentials SET password = '{password}' WHERE email='{email}'")
    
    def set_code(self, email: str, code: str):
        self.query(f"UPDATE credentials SET code='{code}' WHERE email='{email}'")
        
    def set_csrf(self, email: str, csrf: str):
        self.query(f"UPDATE credentials SET csrf='{csrf}' WHERE email='{email}'")
        
    def check_code(self, email: str, code: str):
        cursor_res = self.query(f"SELECT code FROM credentials WHERE email='{email}'")
        print(code, type(code), cursor_res[0][0], type(cursor_res[0][0]))
        if cursor_res:
            return cursor_res[0][0] == code
        return None
    
    def get_salt(self, email: str):
        cursor_res = self.query(f"SELECT salt FROM credentials WHERE email='{email}'")
        if cursor_res:    
            return cursor_res[0][0]
        return None
    
    def check_csrf(self, email: str, csrf):
        cursor_res = self.query(f"SELECT csrf FROM credentials WHERE email='{email}'")
        if cursor_res:    
            return cursor_res[0][0] == csrf
        return None
    
    def update_products(self, products_list: dict):
        self.query(f'DELETE FROM catalog *')        
        for shop in list(products_list.keys()):
            for i in range(len(products_list[shop])):
                for product_key in list(products_list[shop][i].keys()):
                    if isinstance(products_list[shop][i][product_key], str):
                        products_list[shop][i][product_key] = products_list[shop][i][product_key].replace("'", '`').replace('"', '`')
                str_products = str(products_list[shop][i]).replace('\'', '"')
                self.query(f"INSERT INTO catalog (shop, product) VALUES('{shop}', '{str_products}')")        

    def get_products(self, shops_list):
        cursor_res = self.query(f"SELECT product FROM catalog WHERE shop IN {str(shops_list).replace('[', '(').replace(']', ')')}")
        products = [x[0] for x in cursor_res]
      
        return products
        
    def get_page(self, shops_list: list, page_num: int):
        # OFFSET (page_num - 1)*10 LIMIT 10
        total_count = self.query(f"SELECT COUNT(*) FROM (SELECT product FROM catalog WHERE shop IN {str(shops_list).replace('[', '(').replace(']', ')')}) as WECAN")
        cursor_res = self.query(f"SELECT product from (SELECT product FROM catalog WHERE shop IN {str(shops_list).replace('[', '(').replace(']', ')')}) as foo  OFFSET {(page_num - 1) * 10} LIMIT 10")
        products = [x[0] for x in cursor_res]
        return products, total_count[0][0]