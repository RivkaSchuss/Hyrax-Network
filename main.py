import HelperMethods
import datetime
import ParseDetails
from scipy.sparse import lil_matrix
from scipy import sparse
import numpy as np
import json
import csv


def main():
    # HelperMethods.save_encounters_to_files()

    personal_list = [2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 19, 21, 22, 23, 24, 25, 26, 29, 33, 36, 39]
    calculated_list = []
    HelperMethods.run_all_pairs(personal_list, calculated_list)


if __name__ == '__main__':
    main()

    # s = HelperMethods.amount_of_seconds
    # for i in range(s):
    #     if mtx_1[0, i] != 0:
    #         a_to_b += 1
    #     if mtx_2[0, i] != 0:
    #         b_to_a += 1
    #     if mtx_1[0, i] != 0 and mtx_2[0, i] != 0:
    #         a_xor_b += 1
    #     if mtx_1[0, i] != 0 or mtx_2[0, i] != 0:
    #         a_union_b += 1
    #
    # print(a_to_b)
    # print(b_to_a)
    # print(a_union_b)
    # print(a_xor_b)
# k = 0
# for key, val in pair_to_row_dict.items():
#     mtx = lil_matrix((1, HelperMethods.amount_of_seconds))
#     personal, other_hyrax = key
#     filename = HelperMethods.get_npz_file_name(personal, other_hyrax)
#     if personal == 2 and other_hyrax == 26:
#
#         for e in encounters_list:
#             k += 1
#             if e.personal_id == personal and int(e.enc_id) == other_hyrax:
#                 i, j = HelperMethods.get_columns_indexes_by_time(start_experiment_date, e.full_date, e.length)
#                 t = tuple([personal, other_hyrax])
#                 # row = pair_to_row_dict[t]
#                 HelperMethods.add_values_to_lil(mtx, 0, i, j)
#         save_lil(filename, mtx)

# if personal in personal_list and other_hyrax in personal_list:
#     i, j = HelperMethods.get_columns_indexes_by_time(start_experiment_date, e.full_date, e.length)
#     t = tuple([personal, other_hyrax])
#     row = pair_to_row_dict[t]
#     HelperMethods.add_values_to_lil(mtx, row, i, j)

# mtx = lil_matrix((20, 20))
# for i in range(20):
#     HelperMethods.add_values_to_lil(mtx, i, 4, 8)

# filename = 'LIL' + str(personal) + str(other_hyrax) + '.npz'

# filename = 'LIL.npz'
#
# save_lil(filename, mtx)
# loaded_mtx = load_lil(filename)
# print(loaded_mtx)
