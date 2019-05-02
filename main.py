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
    # calculated_list = [4, 11, 24, 33, 39]
    calculated_list = [4, 11, 24]

    lr.learn(calculated_list)
    # with open('dataSet.csv', 'a') as outcsv:
    #     writer = csv.writer(outcsv)
    #     writer.writerow(["pair", "1_day_meet_count", "1_night_meet_count", "Sex", "did_meet"])

    print("d")


if __name__ == '__main__':
    main()
