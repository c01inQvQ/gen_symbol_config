import unittest
from common.options_codes import get_settlement_date, gen_options_codes


class TestOptionsCodes(unittest.TestCase):
    def setUp(self):
        self.test_data1 = {
            '2018-04-17': [None, '201804'],
            '2018-04-18': ['201804', '201804W4'],
            '2018-12-26': ['201812W4', '201901W1'],
            '2019-04-05': [None, '201904W2'],
            '2019-04-10': ['201904W2', '201904']
        }
        self.test_data2 = [
            '201804',
            '201804W4',
            '201912W4',
            '201901W1',
            '201904W2',
            '201904',
            None,
        ]
        self.test_data3 = {
            '201804': 'TXO',
            '201804W4': 'TX4',
            '201912W4': 'TX4',
            '201901W1': 'TX1',
            '201904W2': 'TX2',
            '201904': 'TXO',
        }
        self.test_data4 = {
            '201804': ['D', 'P'],
            '201804W4': ['D', 'P'],
            '201912W4': ['L', 'X'],
            '201901W1': ['A', 'M'],
            '201904W2': ['D', 'P'],
            '201911': ['K', 'W'],
        }
        self.test_data5 = {
            '201804': '8',
            '201804W4': '8',
            '201912W4': '9',
            '201901W1': '9',
            '201904W2': '9',
            '201911': '9',
        }

    def test_get_settlement_date(self):
        for date, settlement_dates in self.test_data1.items():
            old_settlement_date, new_settlement_date = get_settlement_date(date)
            self.assertEqual([old_settlement_date, new_settlement_date], settlement_dates)

    def test_options_codes_length(self):
        for settlement_date in self.test_data2:
            options_codes_list = gen_options_codes(settlement_date)
            if settlement_date is None:
                self.assertEqual(len(options_codes_list), 0)
            else:
                self.assertNotEqual(len(options_codes_list), 0)
                for options_code in options_codes_list:
                    self.assertEqual(len(options_code), 10)

    def test_options_codes_week(self):
        for settlement_date, week_code in self.test_data3.items():
            options_codes_list = gen_options_codes(settlement_date)
            for options_code in options_codes_list:
                self.assertEqual(options_code[0:3], week_code)

    def test_options_codes_month(self):
        for settlement_date, month_code_list in self.test_data4.items():
            options_codes_list = gen_options_codes(settlement_date)
            for options_code in options_codes_list:
                self.assertTrue(options_code[8:9] in month_code_list)

    def test_options_codes_year(self):
        for settlement_date, year_code in self.test_data5.items():
            options_codes_list = gen_options_codes(settlement_date)
            for options_code in options_codes_list:
                self.assertEqual(options_code[9:10], year_code)


if __name__ == '__main__':
    unittest.main()
