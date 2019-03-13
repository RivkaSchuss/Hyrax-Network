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
    # HelperMethods.save_encounters_to_files()
    personal_list = [2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 19, 21, 22, 23, 24, 25, 26, 29, 33, 36, 39]
    # personal_list = [4, 6, 8, 11, 12, 14, 19, 21, 22, 23, 24, 25, 26, 29, 33, 36, 39]
    calculated_list = []
    # h.run_diff_per_days_for_all_pairs(personal_list, calculated_list)
    encounters_count_dic = h.read_encounters_count()

    # h.run_diff_per_days_for_all_pairs(personal_list, calculated_list)
    offset_max_dic = h.find_offset_to_maximize_agreement()
    offset_fixed = h.fix_offset(offset_max_dic, encounters_count_dic)

    offset_list = []
    # for key, val in offset_max_dic.items():
        # if val != 'null':
        #     value = int(val)
            # offset_list.append(val)
            # if value > 55:
            #     print(key, value)
            #     key = tuple(key)
            #     key_2 = (int(key[0]), int(key[1]))
            #     rev_key = tuple(reversed(key_2))
                # calculated_list.remove(rev_key)
                # calculated_list.remove(key_2)
            # if value < -58:
            #     print(key, value)
            #     key = tuple(key)
            #     key_2 = (int(key[0]), int(key[1]))
            #     rev_key = tuple(reversed(key_2))
                # calculated_list.remove(rev_key)
                # calculated_list.remove(key_2)
    me = np.mean(offset_list)
    print(me)
    med = median(offset_list)
    print(med)
    print(offset_list)
    # h.run_diff_per_days_for_all_pairs(personal_list, calculated_list)


if __name__ == '__main__':
    main()
