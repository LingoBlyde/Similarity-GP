import csv
import os

html_header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<table>
"""

html_body = """<tr>
    <td width="100">id: %s</td>
    <td width="100">dhash: %s</td>
    <td><img width=150px src="%s"></td>
    <td><img width=150px src="%s"></td>
</tr>
"""

html_footer = """</table>
</body>
</html>
"""


def generate_report(raw_file_name, report_file_name):
    if os.path.exists(report_file_name):
        os.remove(report_file_name)

    with open(report_file_name, 'a') as writer:
        writer.write(html_header)
        for icon_id, old, new, similarity in read_data(raw_file_name):
            writer.write(html_body % (icon_id, similarity, old, new))
            print 'ok for %s' % icon_id
        writer.write(html_footer)


def read_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for icon_id, old_val, new_val, similarity in reader:
            yield icon_id, old_val, new_val, similarity


if __name__ == '__main__':
    raw_file = 'res/icon/report_test_icons.csv'
    report_file = 'res/icon/report_icon_test.html'
    generate_report(raw_file, report_file)
    print 'Succeed to finish.'
