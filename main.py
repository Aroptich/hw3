import pymysql

from config import host, port, user, password, schema_name






class Database:


    @staticmethod
    def connect(func):
        def wrapper(*args, **kwargs):
            try:
                connection = pymysql.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    database=schema_name,
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("successfully connected....")
                with connection.cursor() as cursor:
                    cursor.execute(func(*args, **kwargs))
                    connection.commit()
            except Exception as err:
                print("Connection refused...")
                print(err)
            finally:
                connection.close()

        return wrapper




if __name__ == '__main__':
   db= Database()