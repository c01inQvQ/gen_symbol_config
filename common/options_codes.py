import psycopg2
import datetime
from rules import rules
from rules.settlement_dates import settlement_dates
from configs.config import pgsql_config
sql_destination = 'host={} dbname={} user={} password={}'.format(pgsql_config['host'], pgsql_config['dbname'], pgsql_config['user'], pgsql_config['password'])


def get_settlement_date(date):
    if date in settlement_dates:
        old_settlement_date = settlement_dates[date]
        next_index = list(settlement_dates.keys()).index(date) + 1
        new_settlement_date = list(settlement_dates.values())[next_index]

    else:
        old_settlement_date = None
        date_list = list(settlement_dates.keys())
        date_list.append(date)
        date_list.sort()
        next_index = date_list.index(date)
        new_settlement_date = list(settlement_dates.values())[next_index]

    return old_settlement_date, new_settlement_date


def gen_options_codes(settlement_date):
    try:
        if settlement_date is None:
            return []

        options_codes_list = []

        year_code = settlement_date[3:4]
        month_code = rules.options_month_dict[settlement_date[4:6]]
        week_code = rules.options_week_dict[settlement_date[6:8]]

        conn = psycopg2.connect(sql_destination)
        cur = conn.cursor()
        sql_query = """
        SELECT last
        FROM api_taifex_futures_price
        WHERE date < '{date}' AND contract = 'TX' AND session = 'regular'
        ORDER BY date DESC, contract_month
        limit 1
        """

        today = datetime.datetime.today().strftime('%Y-%m-%d')
        cur.execute(sql_query.format(date=today))
        close_price = int(cur.fetchone()[0])

        for cp in ['Call', 'Put']:
            lower_bound = (close_price - 400) // 100 * 100
            upper_bound = (close_price + 400) // 100 * 100
            while lower_bound <= upper_bound:
                    options_code = week_code + str(lower_bound).zfill(5) + month_code[cp] + year_code
                    options_codes_list.append(options_code)
                    lower_bound += 50

        return options_codes_list

    except:
        raise


