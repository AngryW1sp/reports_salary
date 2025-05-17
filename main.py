import argparse
from engine import Engine, read_csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='CSV-файлы с данными')
    parser.add_argument('--directory', help='Директория с файлами CSV, '
                        'по умолчанию файлы находятся в папке с исполняющим файлом')
    parser.add_argument('--report',  help='Тип отчёта')
    parser.add_argument(
        '--format', help='Формат вывода данных, по умолчанию JSON')
    args = parser.parse_args()

    for file in args.files:
        path = f"{args.directory}/{file}" if args.directory else file
        try:
            data = read_csv(path)
        except Exception as e:
            print(f"[Ошибка]: {e}")
            return

        if not args.report and not args.format:
            try:
                print(Engine.generate_format('json', data))
            except Exception as e:
                print(f"[Ошибка при генерации данных]: {e}")

        elif not args.report and args.format:
            try:
                print(Engine.generate_format(args.format, data))
            except Exception as e:
                print(f"[Ошибка при генерации данных]: {e}")
        elif args.report and not args.format:
            try:
                print(Engine.generate_report(args.report, data))
            except Exception as e:
                print(f"[Ошибка при генерации отчёта]: {e}")
        else:
            try:
                try:
                    print(Engine.generate_report(args.report, data))
                except Exception as e:
                    print(f"[Ошибка при генерации отчёта]: {e}")
                try:
                    print(Engine.generate_format(args.format, data))
                except Exception as e:
                    print(f"[Ошибка при генерации данных]: {e}")

            except Exception as e:
                print(f"Ошибка: {e}")
        print('_'*30)


if __name__ == '__main__':
    main()
