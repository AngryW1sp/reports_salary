from engine import generate_payout_report


def test_payout_report():
    test_data = [{'name': 'Test', 'department': 'IT',
                  'hours_worked': '100', 'hourly_rate': '10'}]
    assert '--------------------------------- \n\n\nИмя: Test,  Депортамент: IT ---> Зарплата: 1000\n\n\n--------------------------------- ' in generate_payout_report(
        test_data)
