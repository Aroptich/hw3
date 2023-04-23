from dataclasses import dataclass

@dataclass
class Eployee:
    firstname: str
    lastname: str
    post: str
    seniority: int
    salary: int
    age: int

employee1 = Eployee('"Вася"', '"Петров"', '"Начальник"', 40, 100000, 60)
employee2 = Eployee('"Петр"', '"Власов"', '"Начальник"', 8, 70000, 30)
employee3 = Eployee('"Катя"', '"Катина"', '"Инженер"', 2, 70000, 25)
employee4 = Eployee('"Саша"', '"Санин"', '"Инженер"', 12, 50000, 35)
employee5 = Eployee('"Иван"', '"Иванов"', '"Рабочий"', 40, 30000, 59)
employee6 = Eployee('"Петр"', '"Петров"', '"Рабочий"', 20, 25000, 40)
employee7 = Eployee('"Сидр"', '"Сидоров"', '"Рабочий"', 10, 20000, 35)
employee8 = Eployee('"Антон"', '"Антонов"', '"Рабочий"', 8, 19000, 28)
employee9 = Eployee('"Юрий"', '"Юрков"', '"Рабочий"', 5, 15000, 25)
employee10 = Eployee('"Максим"', '"Максимов"', '"Рабочий"', 2, 11000, 24)
employee11 = Eployee('"Юрий"', '"Галкин"', '"Рабочий"', 3, 12000, 24)
employee12 = Eployee('"Людмила"', '"Маркина"', '"Уборщик"', 10, 10000, 49)

employees =[employee1,
            employee2,
            employee3,
            employee4,
            employee5,
            employee6,
            employee7,
            employee8,
            employee9,
            employee10,
            employee11,
            employee12]
