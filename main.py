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

    @connect
    def create_table(self, table_name: str, **dict_data: dict) -> str:
        try:
            self.table_name = table_name
            self.columns_name = [keys for keys in dict_data]
            self.type_data = [dict_data[keys] for keys in dict_data]
            self.res = ','.join([' '.join(i) for i in zip(self.columns_name, self.type_data)])
            self.create_table_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({self.res});"
            return self.create_table_query
        except Exception as err:
            print(err)


if __name__ == '__main__':
    db = Database()
    create_table = db.create_table('staff',
                                   id='int auto_increment primary key',
                                   firstname='varchar(40)',
                                   lastname='varchar(40)',
                                   post='varchar(40)',
                                   seniority='int',
                                   salary='int',
                                   age='int')

