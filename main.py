import pymysql
from prettytable import PrettyTable
from datetime import datetime

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
                    res = cursor.execute(func(self, *args, **kwargs))
                    if res <= 0:
                        print(f'Данных не найдено!')
                        return None
                    x = PrettyTable()
                    rows = cursor.fetchall()
                    x.field_names = [row for row in rows[0]]
                    for row in rows:
                        x.add_row([row[i] for i in row])
                    print(x)
                    connection.commit()
                    return res
            except Exception as err:
                print("Connection refused...")
                print(err)
            finally:
                connection.close()

        return wrapper

    @staticmethod
    def logger(func):
        def wrapper(*args, **kwargs):
            try:
                with open('log.txt', 'a', encoding='utf-8') as file:
                    query = func(*args, **kwargs)
                    file.writelines(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                    file.writelines(f"{'=' * 35}\n")
                    file.writelines(f'{query}\n')
                    file.writelines(f"{'=' * 35}\n")
                    return query
            except Exception as err:
                print(err)

        return wrapper

    @connect
    @logger
    def create_table(self, table_name: str, **dict_data: dict) -> str:
        try:
            self.table_name = table_name
            self.columns_name = [keys for keys in dict_data]
            self.type_data = [dict_data[keys] for keys in dict_data]
            self.res = ',\n'.join([' '.join(i) for i in zip(self.columns_name, self.type_data)])
            self.create_table_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} \n({self.res});"
            return self.create_table_query
        except Exception as err:
            print(err)

    @connect
    @logger
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
    @logger
    def sort_columns(self, table_name: str, column_name: str, sort=True, limit=None) -> str:
        try:
            self.table_name = table_name
            self.columns_name = column_name
            if not sort and limit is None or limit == 0:
                self.sort_columns_query = f"SELECT * \nFROM {self.table_name} \nORDER BY {self.columns_name} DESC;"
                return self.sort_columns_query
            elif not sort and limit:
                self.sort_columns_query = f"SELECT * \nFROM {self.table_name} \nORDER BY {self.columns_name} DESC \nLIMIT {limit};"
                return self.sort_columns_query
            elif sort and limit > 0:
                self.sort_columns_query = f"SELECT * \nFROM {self.table_name} \nORDER BY {self.columns_name} \nLIMIT {limit};"
                return self.sort_columns_query
            else:
                self.sort_columns_query = f"SELECT * \nFROM {self.table_name} \nORDER BY {self.columns_name};"
                return self.sort_columns_query

        except Exception as err:
            print(err)

    @connect
    @logger
    def select_data(self, table_name: str, **kwargs) -> str:
        try:
            self.name_table = table_name
            self.select_all_rows = f"SELECT * FROM {self.name_table}"
            return self.select_all_rows
        except Exception as err:
            print(err)

    @reading_data
    @logger
    def total_salary_by_post(self, table_name: str, post: str) -> str:
        try:
            self.table_name = table_name
            self.post = post
            self.total_salary_by_post_query = f"SELECT SUM(salary) AS `Суммарная зарплата на должности {self.post}` " \
                                              f"FROM {self.table_name} " \
                                              f"WHERE post={self.post}"
            return self.total_salary_by_post_query
        except Exception as err:
            print(err)

    @reading_data
    @logger
    def count_posts(self, table_name: str, column_name: str, post: str) -> str:
        try:
            self.table_name = table_name
            self.post = post
            self.columns_name = column_name
            self.count_posts_query = f"SELECT COUNT({self.columns_name}) AS 'Найдено совпадений' " \
                                     f"\nFROM {self.table_name} " \
                                     f"\nWHERE post={self.post} AND age between 29 and 49;"
            return self.count_posts_query
        except Exception as err:
            print(err)

    @reading_data
    @logger
    def count_of_posts(self, table_name: str, column_name: str, post: str) -> str:
        try:
            self.table_name = table_name
            self.post = post
            self.columns_name = column_name
            self.count_of_posts_query = f"SELECT COUNT({self.columns_name}) AS 'Найдено совпадений {self.post}' " \
                                        f"\nFROM {self.table_name} " \
                                        f"\nWHERE post={self.post};"

            return self.count_of_posts_query
        except Exception as err:
            print(err)

    @reading_data
    @logger
    def avg_age_of_employee(self, table_name: str, column_name: str) -> str:
        try:
            self.table_name = table_name
            self.columns_name = column_name
            self.count_of_posts_query = f"SELECT {self.columns_name} AS 'Специальности, где средний возраст < 30 лет' " \
                                        f"\nFROM {self.table_name} " \
                                        f"\nGROUP BY {self.columns_name} " \
                                        f"\nHAVING AVG(age) < 30;"

            return self.count_of_posts_query
        except Exception as err:
            print(err)


if __name__ == '__main__':
    db = Database()
    # Создание таблицы
    create_table = db.create_table('staff',
                                   id='int auto_increment primary key',
                                   firstname='varchar(40)',
                                   lastname='varchar(40)',
                                   post='varchar(40)',
                                   seniority='int',
                                   salary='int',
                                   age='int')
    # Добавление данных в таблицу
    for employee in employees:
        insert_note = db.insert_data('staff', employee.__dict__)
    # Сортировка данных по полю заработная плата (salary) в порядке: убывания; возрастания
    db.sort_columns('staff', 'salary', sort=True)
    # Вывод 5 максимальных заработных плат (saraly)
    db.sort_columns('staff', 'salary', sort=True, limit=5)
    # Подсчет суммарной зарплаты (salary) по каждой специальности (роst)
    db.total_salary_by_post('staff', '"Рабочий"')
    db.total_salary_by_post('staff', '"Начальник"')
    db.total_salary_by_post('staff', '"Инженер"')
    db.total_salary_by_post('staff', '"Уборщик"')
    # Кол-во сотрудников с специальностью (post) «Рабочий» в возрасте от 24 до 49 лет включительно.
    db.count_posts('staff', 'post', '"Рабочий"')
    # Нахождение количество специальностей
    db.count_of_posts('staff', 'post', '"Рабочий"')
    db.count_of_posts('staff', 'post', '"Начальник"')
    db.count_of_posts('staff', 'post', '"Инженер"')
    db.count_of_posts('staff', 'post', '"Уборщик"')
    # Вывод специальностей, у которых средний возраст сотрудников меньше 30 лет
    db.avg_age_of_employee('staff', 'post')
