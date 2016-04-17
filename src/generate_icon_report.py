import argparse
import csv
import os

import imagehash

from icon_spider import UrlLibIconSpider


def generate_report(begin_id, raw_file_name, report_file_name):
    if os.path.exists(report_file_name):
        os.remove(report_file_name)
    icon_spider = UrlLibIconSpider()
    with open(report_file_name, 'a') as report_file:
        writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for icon_id, old, new in read_raw_data(raw_file_name):
            if int(icon_id) < begin_id:
                continue
            similarity = compute_similarity(icon_spider, old, new)
            save(writer, [icon_id, old, new, similarity])
            print 'ok for %s, similarity: %s' % (icon_id, similarity)


def read_raw_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for icon_id, old_val, new_val in reader:
            yield icon_id, old_val, new_val


def compute_similarity(icon_spider, base_val, comparison_val):
    url_icon_set = icon_spider.scrape({base_val, comparison_val})
    if not any(url_icon_set.values()) or base_val not in url_icon_set or comparison_val not in url_icon_set:
        return 'N/A'
    try:
        similarity = abs(imagehash.dhash(url_icon_set[base_val]) - imagehash.dhash(url_icon_set[comparison_val]))
        return similarity
    except Exception as ex:
        print ex
        return 'N/A'


def save(writer, row):
    """

    :param writer:
    :param row:
    :return:
    """
    writer.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--filename', dest='filename', type=str,
        help='Name of file in res/icon'
    )
    parser.add_argument(
        '--after', dest='after', type=int, default=0,
        help='after id'
    )
    args = parser.parse_args()
    raw_file = 'res/icon/ios_icon_%s.csv' % args.filename
    report_file = 'res/icon/report_ios_icon_%s.csv' % args.filename
    generate_report(args.after, raw_file, report_file)
    print 'Succeed to finish.'
