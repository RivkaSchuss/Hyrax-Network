# import HelperMethods as h
import datetime
import ParseDetails as pd
from scipy.sparse import lil_matrix
from scipy import sparse
import numpy as np
from statistics import median
import json
import csv

from sklearn.datasets import load_iris
from sklearn import tree
import pydotplus
import itertools


def main():
    # hyrax_list = [2, 7]

    # import HelperMethods as h
    hyrax_list = [2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 19, 21, 22, 23, 24, 25, 26, 29, 33, 36, 39]
    last_n_days = [1, 10]
    # h.run_diff_per_days_for_all_pairs(hyrax_list, [], 190)
    # offset_dictionary = h.find_offset_to_maximize_agreement()
    # h.fix_offset(offset_dictionary, 'LIL_mtx_fixed')

    # h.save_encounters_to_files('LIL_mtx')
    # lr.make_db_by_hours(hyrax_list)
    # lr.hours_train(hyrax_list)

    import Learning as lr
    lr.make_db_and_train_by_hours(hyrax_list)

    # lr.save_count_per_hour_to_file(hyrax_list)
    # lr.make_db_and_train(hyrax_list,
    #          last_n_list=last_n_days, sex=True, group=False,
    #          canyon=False, should_make_graph=True)

    # lr.save_count_per_day_to_file(hyrax_list, None)
    print("Done")


if __name__ == '__main__':
    main()
