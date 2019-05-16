import HelperMethods as h
import datetime
import ParseDetails as pd
from scipy.sparse import lil_matrix
from scipy import sparse
import numpy as np
from statistics import median
import json
import csv
import Learning as lr
from sklearn.datasets import load_iris
from sklearn import tree
import pydotplus
import itertools


def main():
    personal_list = [2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 19, 21, 22, 23, 24, 25, 26, 29, 33, 36, 39]
    # calculated_list = [4, 11, 24, 33, 39]

    last_n_days = [9, 10]
    lr.make_db_for_tree(personal_list, last_n_days)
    lr.train(personal_list, last_n_days)

    # perm = list(itertools.combinations([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4))
    # results = []
    # for p in perm:
    #     lr.db_global_name = 'DB/data_{}.csv'.format(datetime.datetime.now().strftime("%H%M_%S%f_%B_%d_%Y"))
    #     lr.make_db_for_tree(personal_list, p)
    #     results.append(lr.train(personal_list, p, False))
    #
    # print(results)
    # print(max(results))
    print("done")


if __name__ == '__main__':
    main()
