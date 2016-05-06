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
    <td width="100">id: {id}</td>
    <td width="100">tag: {tag}</td>
    <td><img width=150px src="{old}"></td>
    <td><img width=150px src="{new}"></td>
</tr>
"""

html_footer = """</table>
</body>
</html>
"""


def generate_report(dir_path, raw_file_name, report_file_name):
    if os.path.exists(report_file_name):
        os.remove(report_file_name)

    with open(report_file_name, 'a') as writer:
        writer.write(html_header)
        for icon_id, similarity, tag in read_data(raw_file_name):
            old = dir_path + '/{id}/left.png'.format(id=icon_id)
            new = dir_path + '/{id}/ight.png'.format(id=icon_id)
            writer.write(html_body.format(id=icon_id, tag=tag, old=old, new=new))
            print 'ok for %s' % icon_id
        writer.write(html_footer)


def read_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for icon_id, _, _, similarity, tag in reader:
            yield icon_id, similarity, tag


if __name__ == '__main__':
    dir_path = 'd:/workspace/workspace/icons'
    raw_file = 'res/icon/icons_sort.csv'
    report_file = 'res/icon/icons_sort.html'
    generate_report(dir_path, raw_file, report_file)
    print 'Succeed to finish.'
