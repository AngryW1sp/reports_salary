from collections import defaultdict
from formatters.base import json_formatter


def read_csv(file_path: str) -> list[dict[str, str]]:
    """""
    В этой функции происходит чтение CSV-файла
    - Получаем заголовок файла
    - Построчно читаем файл и через zip объеденям данные с заголовком
    - На выходе получаем список словарей с упорядоченными данными
    """""
    with open(file_path, 'r', encoding='utf-8') as f:
        headers = f.readline().strip().split(',')
        if not headers or all(not column for column in headers):
            raise ValueError(
                f"Файл {file_path} пустой или без заголовков,"
                "или один из заголовков пустой.")
        return [
            dict(zip(headers, line.strip().split(','))) for line in f
        ]


def salary_detection(row: dict) -> str:
    """""
    В этой функции мы сравниваем названия колонок в словаре,
    с извесными названиями зарплатных колонок
    """""
    for column in ['hourly_rate', 'rate', 'salary']:
        if column in row:
            return column
    raise ValueError("Не найдена колонка с зарплатой!")


def generate_payout_report(workers: list[dict]) -> str:
    """""
    Генерация отчёта по выплатам, сгруппированного по департаментам,
    с табличным выводом в стиле, представленном на изображении.
    
    Мы проверяем 
    """""
    departments = defaultdict(list)

    for worker in workers:
        try:
            name = worker['name']
            department = worker['department']
            hours = int(worker['hours_worked'])
            salary_key = salary_detection(worker)
            rate = int(worker[salary_key])
            payout = hours * rate
        except (KeyError, ValueError):
            continue

        departments[department].append({
            'name': name,
            'hours': hours,
            'rate': rate,
            'payout': payout
        })

    report_lines = []

    for department, employees in departments.items():
        report_lines.append(f"{department}")
        total_hours = 0
        total_payout = 0

        for emp in employees:
            report_lines.append(
                f"    ------------- {emp['name']:<15} {emp['hours']:<6} {emp['rate']:<6} ${emp['payout']}")
            total_hours += emp['hours']
            total_payout += emp['payout']

        report_lines.append(
            f"{'':>30}{total_hours:<6}     ${total_payout}\n")

    return "\n".join(report_lines)

class Engine:
    """""
    Наш двигатель:
    Класс Engine, хранит в себе словарь с командами, получаемыми при запуске
    Словарь состоит из строчки - названия команды и функции которая по ней вызывается

    Таким образом при необходимости добавления новых отчетов, мы просто создаем их логику,
    а далее просто добавляем команду в словарь _reports
    Так же добавляются и новые форматы
    """""
    _reports = {
        'payout': generate_payout_report,
    }
    _formats = {
        'json': json_formatter,
    }

    @classmethod
    def generate_report(cls, name: str, data: list[dict]) -> str:
        if name not in cls._reports:
            raise ValueError(f"Отчёт '{name}' не поддерживается!")
        return cls._reports[name](data)

    @classmethod
    def generate_format(cls, name: str, data: list[dict]) -> str:
        if name not in cls._formats:
            raise ValueError(f"Формат '{name}' не поддерживается!")
        return cls._formats[name](data)
