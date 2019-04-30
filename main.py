import HelperMethods as h
import datetime
import ParseDetails
from scipy.sparse import lil_matrix
from scipy import sparse
import numpy as np
from statistics import median
import json
import csv


def main():

    personal_list = [2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 19, 21, 22, 23, 24, 25, 26, 29, 33, 36, 39]
    calculated_list = []
    days = h.initialize_days()
    date_times = h.initialize_specific_range()
    date, time, night = h.get_time_of_day(days, date_times, 3)
    print(date, time, night)


if __name__ == '__main__':
    main()
