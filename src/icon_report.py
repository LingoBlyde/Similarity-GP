import csv

import numpy as np


def generate_report(raw_file_name):
    data = read_data(raw_file_name)
    stat = statistics(data)


def read_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        data = list()
        for icon_id, old_val, new_val, val, tag in reader:
            data.append((icon_id, old_val, new_val, val, tag))
        return data


def statistics(data_list):
    stat = np.zeros(64)
    for icon_id, old_val, new_val, val, tag in data_list:
        stat[int(val)] += 1
    return stat


if __name__ == '__main__':
    generate_report('res/icon/icon_analytical_data.csv')
