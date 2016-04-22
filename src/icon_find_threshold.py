

def find_threshold(file_name, report_name):
    # example: icon_id, dhash_v, phash_v, tag
    data = read_data(file_name)



def sigmoid(inX):
    return 1.0/(1+exp(-inX))


def read_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        data = list()
        for icon_id, dhash_v, phash_v, tag in reader:
            data.append((icon_id, dhash_v, phash_v, tag))
        return data

if __name__ == '__main__':
    find_threshold('res/icon/demo.csv')
