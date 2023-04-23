import pymysql
from prettytable import PrettyTable

from config import host, port, user, password, schema_name
from employee import employees


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

    @staticmethod
    def reading_data(func):

        def wrapper(self, *args, **kwargs):
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
                    cursor.execute(func(self, *args, **kwargs))
                    x = PrettyTable()
                    rows = cursor.fetchall()
                    x.field_names = [row for row in rows[0]]
                    for row in rows:
                        x.add_row([row[i] for i in row])
                    print(x)
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

    @connect
    def insert_data(self, table_name: str, data: dict) -> str:
        try:
            self.table_name = table_name
            self.columns_name = ','.join([keys for keys in data])
            self.values = ','.join([str(data[keys]) for keys in data])
            self.insert_data_query = f"INSERT INTO {self.table_name} ({self.columns_name}) \nVALUES ({self.values});"
            return self.insert_data_query
        except Exception as err:
            print(err)
    @reading_data
    def sort_columns(self, table_name: str, column_name: str, sort=True, limit=None) -> str:
        try:
            self.table_name = table_name
            self.columns_name = column_name
            if not sort and limit is None or limit == 0:
                self.sort_columns_query = f"SELECT * \nFROM {self.table_name} \nORDER BY {self.columns_name} DESC"
                return self.sort_columns_query
            elif not sort and limit:
                self.sort_columns_query = f"SELECT * \nFROM {self.table_name} \nORDER BY {self.columns_name} DESC \nLIMIT {limit}"
                return self.sort_columns_query
            elif sort and limit > 0:
                self.sort_columns_query = f"SELECT * \nFROM {self.table_name} \nORDER BY {self.columns_name} \nLIMIT {limit}"
                return self.sort_columns_query
            else:
                self.sort_columns_query = f"SELECT * \nFROM {self.table_name} \nORDER BY {self.columns_name}"
                return self.sort_columns_query

        except Exception as err:
            print(err)

    @reading_data
    def select_data(self, table_name: str, **kwargs):
        try:
            self.name_table = table_name
            self.select_all_rows = f"SELECT * FROM {self.name_table}"
            return self.select_all_rows
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
    for employee in employees:
        insert_note = db.insert_data('staff', employee.__dict__)

    db.sort_columns('staff', 'salary', sort=True, limit=25)
