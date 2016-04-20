import csv
import os
import numpy as np
from icon_spider import UrlLibIconSpider
from hash_different import different, dhash, phash


def generate_report(raw_file_name, report_file_name):
    if os.path.exists(report_file_name):
        os.remove(report_file_name)

    with open(report_file_name, 'a') as report_file:
        writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        icon_spider = UrlLibIconSpider()
        data = read_data(raw_file_name)
        for d in data:
            icon_img_dict = icon_spider.scrape({d[1], d[2]})
            dhash_v = 'N/A'
            phash_v = 'N/A'
            if d[1] in icon_img_dict and d[2] in icon_img_dict:
                dhash_v = different(dhash(icon_img_dict[d[1]]), dhash(icon_img_dict[d[2]]))
                phash_v = different(phash(icon_img_dict[d[1]]), phash(icon_img_dict[d[2]]))
            d.extend([dhash_v, phash_v])
            # print d
            writer.writerow(d)
            print 'ok for {}, dhash: {}, phash: {}'.format(d[0], dhash_v, phash_v)

        stat_dhash, stat_phash = statistics(data)

def read_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        data = list()
        for icon_id, old_val, new_val, _, tag in reader:
            data.append([icon_id, old_val, new_val, tag])
        return data


def statistics(data_list):
    stat_dhash = np.zeros(64)
    stat_phash = np.zeros(64)

    for icon_id, old_val, new_val, tag, dhash_v, phash_v in data_list:
        stat_dhash[int(dhash_v)] += 1
        stat_phash[int(phash_v)] += 1
    return stat_dhash, stat_phash


if __name__ == '__main__':
    generate_report('res/icon/icon_analytical_data.csv', 'res/icon/icon_analytical_report.csv')
