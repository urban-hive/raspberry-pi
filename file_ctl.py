import json
import datetime


def _get_dust_data(data_path, encoding='utf-8'):
    fp = None
    try:
        fp = open(data_path, 'r+', encoding=encoding)
    except FileNotFoundError:
        fp = open(data_path, 'w+', encoding=encoding)
        json.dump({'data_list': []}, fp)
        fp.close()
        fp = open(data_path, 'r+', encoding=encoding)
    return json.load(fp)


def _write_to_json(json_obj, data_path, encoding='utf-8'):
    fp = open(data_path, 'w+', encoding=encoding)
    json.dump(json_obj, fp)
    fp.close()


def write_dust_data(pm, measured_date=None):
    if pm is None:
        raise AttributeError
    date = measured_date
    if date is None:
        date = str(datetime.datetime.now())
    data = {'pm': pm, 'measured_date': date}
    json_obj = _get_dust_data('dust.json')
    json_obj['data_list'].append(data)
    _write_to_json(json_obj, 'dust.json')
