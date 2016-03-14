import csv
from difflib import SequenceMatcher


def generate_report(raw_file_name, report_file_name):
    with open(report_file_name, 'a') as report_file:
        writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for old, new in read_raw_data(raw_file_name):
            similarity = compute_similarity(old, new)
            save(writer, [old, new, similarity])


def read_raw_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for old_val, new_val in reader:
            yield old_val, new_val


def compute_similarity(base_val, comparison_val):
    return round(SequenceMatcher(None, base_val.strip().lower(), comparison_val.strip().lower()).ratio(), 2)


def save(writer, row):
    writer.writerow(row)


if __name__ == '__main__':
    raw_file_name = '../res/raw_name_event.csv'
    report_file_name = '../res/report_name_event.csv'
    generate_report(raw_file_name, report_file_name)
    print 'Succeed to finish.'

