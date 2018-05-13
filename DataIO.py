import gzip
import csv
import json
import os
import xmltodict
from datetime import datetime


def write_dict_gz(dictionary, namespace):
    start_time = datetime.now()
    with gzip.GzipFile(get_file_path(namespace, 'dict.gz'), 'wb') as file:
        dict_to_json = json.dumps(dictionary)
        file.write(bytes(dict_to_json, 'utf-8'))
        elapsed_time = datetime.now() - start_time
        print('write time: {} for {}'.format(elapsed_time, namespace))


def write_csv(dataset, namespace, header_array, sorted=False):
    start_time = datetime.now()
    with open(get_file_path(namespace, 'csv', sorted), 'w') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(header_array)
        for item in dataset:
            if type(item) is str:
                item = [item]
            writer.writerow(item)
        elapsed_time = datetime.now() - start_time
        print('write time: {} for {}'.format(elapsed_time, namespace))


def get_dict_gz_as_json(namespace):
    start_time = datetime.now()
    with gzip.open(get_file_path(namespace, 'dict.gz'), 'rb') as file:
        file_content = file.read()
        json_loads = json.loads(str(file_content, 'utf-8'))
        elapsed_time = datetime.now() - start_time
        print('load time:  {} for {}'.format(elapsed_time, namespace))
        return json_loads


def parse_owl(owl_name):
    start_time = datetime.now()
    with open(get_file_path(owl_name, 'owl')) as buffered_stream:
        xml_as_dict = xmltodict.parse(buffered_stream.read())

        elapsed_time = datetime.now() - start_time
        print('parse time: {} for {}'.format(elapsed_time, owl_name))
        return xml_as_dict


def write_fma_components(fma, parent, namespace_array):
    for namespace in namespace_array:
        write_dict_gz(fma[parent][namespace], namespace)


def get_file_path(name, file_type, sorted=False):
    return os.getcwd() + '/data%s/%s.%s' % ('/sorted' if sorted else '', format_namespace_for_filename(name), file_type)


def format_namespace_for_filename(namespace):
    return namespace.replace(':', '__')
