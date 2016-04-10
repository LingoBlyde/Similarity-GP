import csv
import os

import imagehash

from icon_spider import UrlLibIconSpider


def generate_report(raw_file_name, report_file_name):
    if os.path.exists(report_file_name):
        os.remove(report_file_name)

    with open(report_file_name, 'a') as report_file:
        writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for icon_id, old, new in read_raw_data(raw_file_name):
            similarity = compute_similarity(old, new)
            save(writer, [icon_id, old, new, similarity])
            print 'ok for %s, similarity: %s' % (icon_id, similarity)


def read_raw_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for icon_id, old_val, new_val in reader:
            yield icon_id, old_val, new_val


def compute_similarity(base_val, comparison_val):
    icon_spider = UrlLibIconSpider()
    url_icon_set = icon_spider.scrape({base_val, comparison_val})
    if not any(url_icon_set.values()):
        return 'N/A'
    similarity = abs(imagehash.dhash(url_icon_set[base_val]) - imagehash.dhash(url_icon_set[comparison_val]))
    return similarity


def save(writer, row):
    """

    :param writer:
    :param row:
    :return:
    """
    writer.writerow(row)


if __name__ == '__main__':
    raw_file = 'res/icon/test_icon.csv'
    report_file = 'res/icon/report_test_icons.csv'
    generate_report(raw_file, report_file)
    print 'Succeed to finish.'
