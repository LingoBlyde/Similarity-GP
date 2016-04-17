import csv

import os

from src.dhash import different, dhash
from src.icon_spider import UrlLibIconSpider


def generate_report(begin_id, raw_file_name, report_file_name):
    if os.path.exists(report_file_name):
        os.remove(report_file_name)
    icon_spider = UrlLibIconSpider()
    with open(report_file_name, 'a') as report_file:
        writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for icon_id, old, new, tag in read_data(raw_file_name):
            if int(icon_id) < begin_id:
                continue
            similarity = compute_similarity(icon_spider, old, new)
            writer.writerow([icon_id, old, new, tag, similarity])
            print 'ok for %s, similarity: %s' % (icon_id, similarity)


def read_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for icon_id, old_val, new_val, _, tag in reader:
            yield icon_id, old_val, new_val, tag


def compute_similarity(icon_spider, base_val, comparison_val):
    url_icon_set = icon_spider.scrape({base_val, comparison_val})
    if not any(url_icon_set.values()) or base_val not in url_icon_set or comparison_val not in url_icon_set:
        return 'N/A'
    try:
        similarity = different(dhash(url_icon_set[base_val], dhash(url_icon_set[comparison_val])))
        return similarity
    except Exception as ex:
        print ex
        return 'N/A'
