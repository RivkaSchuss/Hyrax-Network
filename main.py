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

    # lr.make_histogram(personal_list)

    last_n_days = [10]

    # lr.make_db_by_hours(personal_list)
    # lr.hours_train(personal_list)
    # lr.save_count_per_hour_to_file(personal_list)
    lr.make_db_and_train(personal_list, last_n_list=last_n_days, sex=True, group=False, canyon=False,
                         should_make_graph=True)

    # lr.save_count_per_day_to_file(personal_list, None)
    # perm = list(itertools.combinations([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4))
    print("done")


if __name__ == '__main__':
    main()
