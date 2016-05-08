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
import math
import matplotlib.pyplot as plt


def plotBestFit(dataMat, labelMat, weights=[1,1,1]):
    n = np.shape(dataMat)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if labelMat[i] == 1:
            xcord1.append(dataMat[i,1]); ycord1.append(dataMat[i,2])
        else:
            xcord2.append(dataMat[i,1]); ycord2.append(dataMat[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=25, c='yellow', marker='s')
    ax.scatter(xcord2, ycord2, s=25, c='red')
    x = np.arange(-1.0, 7.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()


def sigmoid(inX):
    sig = 1.0 / (1 + math.exp(-inX))
    return sig


def stocGradAscent0(dataMat, labelMat):
    m, n = np.shape(dataMat)
    alpha = 0.01
    weights = np.ones(n)   #initialize to all ones
    for i in range(m):
        h = sigmoid(sum(dataMat[i] * weights))
        error = labelMat[i] - h
        weights = weights + alpha * error * dataMat[i]
    return weights


def classifyVector(inX, weights):
    prob = sigmoid(sum(inX * weights))
    if prob > 0.5:
        return 1.0
    else:
        return 0.0


def colicTest(dataMat, labelMat):
    trainWeights = stocGradAscent0(dataMat, labelMat)
    errorCount = 0
    numTestVec = len(dataMat)
    for arr, label in zip(dataMat, labelMat):
        if int(classifyVector(arr, trainWeights)) != label:
            errorCount += 1
    errorRate = (float(errorCount) / numTestVec)
    print "the error rate of this test is: %f" % errorRate
    return errorRate


def multiTest(dataMat, labelMat):
    numTests = 5
    errorSum = 0.0
    for k in range(numTests):
        errorSum += colicTest(dataMat, labelMat)
    print "after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests))


def loadDataSet_hash(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        dataMat = list()
        labelMat = list()
        for icon_id, tag, dhash_v, phash_v in reader:
            dataMat.append([1.0, float(dhash_v), float(phash_v)])
            labelMat.append(1) if tag == 'same' else labelMat.append(0)
        return np.array(dataMat), labelMat


def loadDataSet_diff(file_name):
    with file(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        dataMat = list()
        labelMat = list()
        for icon_id, tag, diff in reader:
            dataMat.append([1.0, float(diff)])
            labelMat.append(1) if tag == 'same' else labelMat.append(0)
        return np.array(dataMat), labelMat


if __name__ == '__main__':
    # dataMat, labelMat = loadDataSet('res/icon/ids_hash_report.csv')
    dataMat, labelMat = loadDataSet_diff('res/icon/ids_diff_report.csv')
    multiTest(dataMat, labelMat)

    # weights = stocGradAscent0(dataMat, labelMat)
    # print weights
    # plotBestFit(dataMat, labelMat, weights)
