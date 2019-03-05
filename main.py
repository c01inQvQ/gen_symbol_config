from common.options_codes import get_settlement_date, gen_options_codes
from flask import Flask
from google.cloud import storage
import json
import yaml
import datetime
app = Flask(__name__)


@app.route('/')
def test():
    return 'ok.'


@app.route('/options')
def options():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    old_settlement_date, new_settlement_date = get_settlement_date(today)
    options_codes_list = gen_options_codes(old_settlement_date) + gen_options_codes(new_settlement_date)

    return json.dumps(options_codes_list)


@app.route('/daily_symbol_config')
def daily_symbol_config():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    old_settlement_date, new_settlement_date = get_settlement_date(today)
    options_codes_list = gen_options_codes(old_settlement_date) + gen_options_codes(new_settlement_date)

    with open('./yaml_template/symbol_config.yaml', 'r') as stream:
        docs = yaml.load(stream)
        docs['symbol']['option'] = options_codes_list

    upload_blob('futures-ai-12', yaml.dump(docs, default_flow_style=False), 'application/x-yaml', 'symbol_config.yaml')

    # with open('./symbol_config.yaml', 'w') as stream:
    #     yaml.dump(docs, stream, default_flow_style=False)

    return 'Finished. Yaml file is uploaded to google cloud storage.'


def upload_blob(bucket_name, data, content_type, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data, content_type, None, 'publicRead')
    print('{} uploaded to google cloud storage.'.format(destination_blob_name))


if __name__ == "__main__":
    app.run()
