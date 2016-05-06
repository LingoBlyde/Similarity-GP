import csv
import os
from PIL import Image as PIL_Image

from hash_different import different, dhash, phash


def generate_report(dir_path, raw_file_name, report_file_name):
    if os.path.exists(report_file_name):
        os.remove(report_file_name)

    with open(report_file_name, 'a') as report_file:
        writer = csv.writer(report_file, delimiter=',', quotechar='"')
        data = read_data(raw_file_name)
        for d in data:
            image_obj_left = PIL_Image.open(dir_path + '/{id}/left.png'.format(id=d[0]))
            image_obj_right = PIL_Image.open(dir_path + '/{id}/ight.png'.format(id=d[0]))
            dhash_v = different(dhash(image_obj_left), dhash(image_obj_right))
            phash_v = different(phash(image_obj_left), phash(image_obj_right))
            d.extend([dhash_v, phash_v])
            writer.writerow(d)
            print 'ok for {}, dhash: {}, phash: {}'.format(d[0], dhash_v, phash_v)


def read_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        data = list()
        for icon_id, tag in reader:
            data.append([icon_id, tag])
        return data


if __name__ == '__main__':
    dir_path = 'd:/workspace/workspace/icons'
    generate_report(dir_path, 'res/icon/ids.csv', 'res/icon/ids_hash_report.csv')
