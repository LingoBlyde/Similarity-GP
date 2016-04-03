

icons = list()

with open('gp_icon') as reader:
    for line in reader:
        print line
        infos = line.split('|')
        old, new = infos[5].strip(), infos[6].strip()
        print old, new
        icons.append((old, new))

print icons
import csv
with open('gp_icons.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for row in icons:
        print row
        spamwriter.writerow(row)
