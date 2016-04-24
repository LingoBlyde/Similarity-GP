# import matplotlib.pyplot as plt
# import numpy as np
#
# N=500
# # x = np.random.randn(N)
# # y = np.random.randn(N)
# # xx = np.random.randn(N)
# # yy = np.random.randn(N)
# x = [2,2,4,5,66]
# y = [2,2,4,5,66]
# xx = [1,2,3,4,5,6]
# yy = [2,3,4,5,6,7]
#
# # import  pdb; pdb.set_trace()
#
# plt.scatter(x,y,color='green',edgecolor='none')
# plt.scatter(xx,yy,color='red',edgecolor='none')
#
# plt.show()

import csv
import numpy as np
import matplotlib.pyplot as plt


def find_threshold(file_name):
    # example: icon_id, dhash_v, phash_v, tag
    data = read_data(file_name)
    x_same, y_same = [], []
    x_different, y_different = [], []
    for d in data:
        if d[3] == 'same':
            x, y = x_same, y_same
        else:
            x, y = x_different, y_different
        x.append(int(d[1]))
        y.append(int(d[2]))

    plt.scatter(x_same, y_same, color='green', marker='o')
    plt.scatter(x_different, y_different, color='red',marker='D')
    plt.show()



# def sigmoid(inX):
#     return 1.0/(1+exp(-inX))


def read_data(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        data = list()
        for icon_id, dhash_v, phash_v, tag in reader:
            data.append((icon_id, dhash_v, phash_v, tag))
        return data

if __name__ == '__main__':
    find_threshold('res/icon/train_datas.csv')
