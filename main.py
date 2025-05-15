import argparse
from engine import Engine, read_csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='CSV-файлы с данными')
    parser.add_argument('--directory', help='Директория с файлами CSV, '
                        'по умолчанию файлы находятся в папке с исполняющим файлом')
    parser.add_argument('--report', required=True, help='Тип отчёта')
    args = parser.parse_args()

    data = []
    for file in args.files:
        if not args.directory:
            data.extend(read_csv(file))
        else:
            data.extend(read_csv(args.directory+'/'+file))

        print(Engine.generate(args.report, data))


if __name__ == '__main__':
    main()
