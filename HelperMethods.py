import ICollar
import datetime
import math
from scipy import sparse
from scipy.sparse import lil_matrix
import ParseDetails
import numpy as np


amount_of_seconds = 5270400


def add_all_encounters(hyrax_dict, start_date, end_date):
    encounter_list = []
    for key, hyrax in hyrax_dict.items():
        hyrax.filter_encounters(start_date, end_date)
        filtered_dict = hyrax.get_filtered_encounters()
        for id, encounter in filtered_dict.items():
            encounter_list.append(encounter)

    return encounter_list


def get_by_hours(encounter_list, start, end, time_interval_min=0, time_interval_max=float("inf")):
    count = 0
    # start = start.split(":")
    if end == datetime.time(00, 00, 00):
        end = datetime.time(23, 59, 59)
    for e in encounter_list:
        # print e.full_date
        # print e.full_date.time()
        if start < e.full_date.time() < end:
            if time_interval_min < e.length < time_interval_max:
                count += 1

    return count


def print_in_intervals(encounters_list):
    for i in range(24):
        s = datetime.time(i % 24, 00)
        t = datetime.time((i + 1) % 24, 00)
        count = get_by_hours(encounters_list, s, t)
        print("Between " + str(i) + ":00  to " + str((i + 1)) + ":00 - " + str(count))


def assign_pairs_to_dict(personal_list):
    pair_to_row_dict = {}
    row_count = 0
    for p_id in personal_list:
        count = len(personal_list)
        for i in range(count):
            if p_id != personal_list[i]:
                row_name = tuple([p_id, personal_list[i]])
                # row_name = str(p_id) + "," + str(personal_list[i])
                pair_to_row_dict[row_name] = row_count
                row_count += 1
    return pair_to_row_dict


def get_columns_indexes_by_time(start_date, full_date, length):
    start_index = int((full_date - start_date).total_seconds())
    end_time = full_date + datetime.timedelta(seconds=length)
    end_index = int((end_time - start_date).total_seconds())
    return start_index, end_index


def get_time_from_column_index(start_date, i):
    current_time = start_date + datetime.timedelta(seconds=i)
    return current_time


def add_values_to_lil(lil, row_to_add, i, j):
    if j > amount_of_seconds - 1:
        j = amount_of_seconds - 1
    if i > amount_of_seconds - 1:
        i = amount_of_seconds - 1

    for placed in range(i, j):
        lil[[row_to_add], [placed]] = 1


def get_npz_file_name(num1, num2):
    filename = 'LIL_mtx\\LIL[' + str(num1) + "-" + str(num2) + '].npz'
    return filename


def save_encounters_to_files():
    start_experiment_date = datetime.datetime(2017, 6, 13, 00, 00)
    hyrax_dict, base_station_dict, last_on, first_off = ParseDetails.parse_details()

    encounters_list = add_all_encounters(hyrax_dict, last_on, first_off)

    personal_list = []

    for i in encounters_list:
        id = i.get_personal_id()
        if not personal_list.__contains__(id):
            personal_list.append(id)

    pair_to_row_dict = assign_pairs_to_dict(personal_list)

    k = 0
    for key, val in pair_to_row_dict.items():
        mtx = lil_matrix((1, amount_of_seconds))
        personal, other_hyrax = key
        filename = get_npz_file_name(personal, other_hyrax)
        # if personal == 2:

        for e in encounters_list:
            k += 1
            if e.personal_id == personal and int(e.enc_id) == other_hyrax:
                i, j = get_columns_indexes_by_time(start_experiment_date, e.full_date, e.length)
                t = tuple([personal, other_hyrax])
                # row = pair_to_row_dict[t]
                add_values_to_lil(mtx, 0, i, j)
        save_lil(filename, mtx)


def calc_enc_bet_mtx(mtx_a, mtx_b):
    a_xor_b = 0
    a_union_b = 0
    a_to_b = 0
    b_to_a = 0
    s = amount_of_seconds
    for i in range(s):
        if mtx_a[0, i] != 0:
            a_to_b += 1
        if mtx_b[0, i] != 0:
            b_to_a += 1
        if mtx_a[0, i] != 0 and mtx_b[0, i] != 0:
            a_xor_b += 1
        if mtx_a[0, i] != 0 or mtx_b[0, i] != 0:
            a_union_b += 1
    return a_xor_b, a_union_b, a_to_b, b_to_a


def save_lil(filename, mtx):
    np.savez(filename, dtype=mtx.dtype.str, data=mtx.data, rows=mtx.rows, shape=mtx.shape)


def load_lil(filename):
    loader = np.load(filename)
    result = lil_matrix(tuple(loader["shape"]), dtype=str(loader["dtype"]))
    result.data = loader["data"]
    result.rows = loader["rows"]
    return result
