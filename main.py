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


def main():

    personal_list = [2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 19, 21, 22, 23, 24, 25, 26, 29, 33, 36, 39]
    calculated_list = []

    lr.learn(personal_list)
    # lr.make_db_for_tree(personal_list)

    print("d")


if __name__ == '__main__':
    main()
