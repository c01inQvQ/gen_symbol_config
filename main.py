from settlement_dates import settlement_dates
from options_codes import gen_options_codes
from flask import Flask
from google.cloud import storage
import yaml
import datetime
app = Flask(__name__)


@app.route('/')
def test():
    return 'ok.'


@app.route('/daily_symbol_config')
def daily_symbol_config():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    if today in settlement_dates:
        old_settlement_date = settlement_dates[today]
        next_index = list(settlement_dates.keys()).index(today) + 1
        new_settlement_date = list(settlement_dates.values())[next_index]
        options_codes_list = gen_options_codes(old_settlement_date) + gen_options_codes(new_settlement_date)

    else:
        date_list = list(settlement_dates.keys())
        date_list.append(today)
        date_list.sort()
        next_index = date_list.index(today)
        new_settlement_date = list(settlement_dates.values())[next_index]
        options_codes_list = gen_options_codes(new_settlement_date)

    with open('./symbol_config.yaml', 'r') as stream:
        docs = yaml.load(stream)
        docs['symbol']['option'] = options_codes_list
    with open('./symbol_config.yaml', 'w') as stream:
        yaml.dump(docs, stream, default_flow_style=False)

    return 'Finished'


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


if __name__ == "__main__":
    app.run()