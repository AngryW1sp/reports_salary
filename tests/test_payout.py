import pytest
from engine import read_csv
import os
import tempfile
from engine import generate_payout_report, Engine


def test_read_csv_correct():
    content = "name,department,hours_worked,hourly_rate\nAlice,HR,40,100\n"
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write(content)
        f.seek(0)
        path = f.name

    data = read_csv(path)
    os.remove(path)

    assert len(data) == 1
    assert data[0]['name'] == 'Alice'
    assert data[0]['hourly_rate'] == '100'


def test_read_csv_missing_header():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("\nAlice,HR,40,100\n")
        path = f.name

    with pytest.raises(ValueError):
        read_csv(path)

    os.remove(path)


def test_read_csv_empty_file():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        path = f.name

    with pytest.raises(ValueError):
        read_csv(path)

    os.remove(path)


def test_generate_payout_report_empty_input():
    output = generate_payout_report([])
    assert output == ""


def test_payout_invalid_salary_field():
    data = [{'name': 'John', 'department': 'HR', 'hours_worked': '10'}]
    with pytest.raises(ValueError, match="Не найдена колонка с зарплатой!"):
        Engine.generate_report('payout', data)

