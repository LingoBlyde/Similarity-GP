import argparse
import csv
import os

from icon_spider import UrlLibIconSpider

dir_path = "icons\{id}"
img_path = "icons\{id}\{lr}.png"

def download(begin_id, raw_file_name):
    icon_spider = UrlLibIconSpider()
    for icon_id, old, new in read_raw_data(raw_file_name):
        if int(icon_id) < begin_id:
            continue

        print 'start', icon_id
        if os.path.exists(dir_path.format(id=icon_id)):
            continue

        url_icon_dict = icon_spider.scrape({old, new})
        if old in url_icon_dict and new in url_icon_dict and url_icon_dict[old] and url_icon_dict[new]:
            save(icon_id, url_icon_dict[old], url_icon_dict[new])
        print 'ok for %s' % (icon_id)


def save(icon_id, old_img, new_img):
    os.mkdir(dir_path.format(id=icon_id))
    old_img.save(img_path.format(id=icon_id, lr='left'))
    new_img.save(img_path.format(id=icon_id, lr='ight'))
    print 'saved', icon_id


def read_raw_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for icon_id, old_val, new_val, _, _ in reader:
            yield icon_id, old_val, new_val


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
    raw_file = 'res/icon/icons.csv'
    download(args.after, raw_file)
    print 'Succeed to finish.'
