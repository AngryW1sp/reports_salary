def read_csv(file_path: str) -> list[dict[str, str]]:
    '''''
    В этой функции происходит чтение CSV-файла
    - Получаем заголовок файла
    - Построчно читаем файл и через zip объеденям данные с заголовком
    - На выходе получаем список словарей с упорядоченными данными
    '''''
    with open(file_path, 'r') as f:
        headers = f.readline().strip().split(',')
        return [
            dict(zip(headers, line.strip().split(','))) for line in f
        ]


def salary_detection(row: dict) -> str:
    '''''
    В этой функции мы сравниваем названия колонок в словаре,
    с извесными названиями зарплатных колонок
    '''''
    for column in ['hourly_rate', 'rate', 'salary']:
        if column in row:
            return column
    raise ValueError("Не найдена колонка с зарплатой!")


def generate_payout_report(workers: list[dict]) -> str:
    '''''
    В этой функции мы собираем наш отчет
    По каждому работнику в исходных данных мы:
    - Ищем заралатную колонку
    - Вычисляем итоговую заработную плату
    - Добавляем полученные данные в отчет

    '''''
    report = ['--------------------------------- \n\n']

    for worker in workers:
        salary = salary_detection(worker)
        payout = int(worker['hours_worked']) * int(worker[salary])
        report.append(
            f"Имя: {worker['name']},  Депортамент: {worker['department']} ---> Зарплата: {payout}")

    report.append('\n\n--------------------------------- ')
    return "\n".join(report)


class Engine:
    '''''
    Наш двигатель:
    Класс Engine, хранит в себе словарь с командами, получаемыми при запуске
    Словарь состоит из строчки - названия команды и функции которая по ней вызывается

    Таким образом при необходимости добавления новых отчетов, мы просто создаем их логику,
    а далее просто добавляем команду в словарь _reports
    '''''
    _reports = {
        'payout': generate_payout_report,
    }

    @classmethod
    def generate(cls, name: str, data: list[dict]) -> str:
        if name not in cls._reports:
            raise ValueError(f"Отчёт '{name}' не поддерживается!")
        return cls._reports[name](data)
