import argparse

__author__ = 'Blyde'

import csv
import numpy as np


def multi_test(data_mat, label_mat, r=(0, 100), step=1):
    best_threshold = 0
    lowest_error = 1.0
    for threshold in range(r[0], r[1], step):
        error_num = 0
        for i in range(1, len(label_mat)):
            if (data_mat[i] <= threshold and label_mat[i] == 0) or (data_mat[i] > threshold and label_mat[i] == 1):
                error_num += 1
        error_rate = float(error_num) / len(label_mat)
        print "threshold: %d the error rate of this test is: %f" % (threshold, error_rate)

        if lowest_error > error_rate:
            best_threshold = threshold
            lowest_error = error_rate
    print 'best threshold: {}, lowest error: {}'.format(best_threshold, lowest_error)


def load_diff_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        data_mat = list()
        label_mat = list()
        for icon_id, tag, diff in reader:
            data_mat.append(int(1000 * float(diff)))
            # data_mat.append(int(diff))
            label_mat.append(1) if tag == 'same' else label_mat.append(0)
        return np.array(data_mat), label_mat


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--filename', dest='filename', type=str, default=1,
        help='Name of file in res/icon'
    )
    args = parser.parse_args()
    # dataMat, labelMat = load_diff_data('res/icon/ids_phash_report.csv')
    dataMat, labelMat = load_diff_data('res/icon/ids_diff_gray_{}_report.csv'.format(args.filename))
    multi_test(dataMat, labelMat, (0, 1000))
