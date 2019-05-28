import ICollar
import datetime
import math
from scipy import sparse
from scipy.sparse import lil_matrix
import ParseDetails
import numpy as np
import csv
import os
import ephem
import time

amount_of_seconds = 5270400
length_of_day = 86400


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
    filename = 'LIL_mtx//LIL[' + str(num1) + "-" + str(num2) + '].npz'
    # filename = 'LIL_mtx\\LIL[' + str(num1) + "-" + str(num2) + '].npz'
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
    end = 86400
    val = 0
    values_per_day = dict()
    for i in range(60):
        a_xor_b, a_union_b, a_to_b, b_to_a = calc_per_day(end, mtx_a, mtx_b)
        if a_xor_b and a_union_b:
            val = a_xor_b / a_union_b
            values_per_day[i + 1] = val
        else:
            values_per_day[i + 1] = 0
        end += 86400
    return values_per_day


def calc_per_day(end, mtx_a, mtx_b):
    a_xor_b = 0
    a_union_b = 0
    a_to_b = 0
    b_to_a = 0
    non_zero_a = mtx_a.nonzero()[1]
    non_zero_b = mtx_b.nonzero()[1]

    for value_a in non_zero_a:
        if value_a > end or value_a < end - 86400:
            continue
        a_to_b += 1
        a_union_b += 1
        if value_a in non_zero_b:
            a_xor_b += 1
            b_to_a += 1
    for value_b in non_zero_b:
        if value_b > end or value_b < end - 86400:
            continue
        if value_b not in non_zero_a:
            b_to_a += 1
            a_union_b += 1

    return a_xor_b, a_union_b, a_to_b, b_to_a


def run_all_pairs_per_day(personal_list, calc_list):
    calculated_list = calc_list
    for i in personal_list:
        for j in personal_list:
            if i != j:
                if (i, j) not in calculated_list:
                    file_a = get_npz_file_name(i, j)
                    file_b = get_npz_file_name(j, i)
                    mtx_a = load_lil(file_a)
                    mtx_b = load_lil(file_b)
                    # a_xor_b, a_union_b, a_to_b, b_to_a = calc_enc_bet_mtx(mtx_a, mtx_b)
                    values_per_day = calc_enc_bet_mtx(mtx_a, mtx_b)
                    row_1 = [str(i) + '->' + str(j)]
                    if values_per_day:
                        print(values_per_day)
                        for key, value in values_per_day.items():
                            row_1.append(value)

                    calculated_list.append((i, j))
                    calculated_list.append((j, i))
                    # row_1 = [str(i) + '->' + str(j)]

                    # row_1 = [str(i) + '->' + str(j), a_xor_b, a_union_b, a_to_b, b_to_a]
                    # row_2 = [str(j) + '->' + str(i), a_xor_b, a_union_b, b_to_a, a_to_b]
                    with open('EncountersInfoPerDay.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(row_1)
                        # writer.writerow(row_2)
                        print(row_1)
                        # print(row_2)


def run_all_pairs(personal_list, calc_list):
    calculated_list = calc_list
    for i in personal_list:
        for j in personal_list:
            if i != j:
                if (i, j) not in calculated_list:
                    file_a = get_npz_file_name(i, j)
                    file_b = get_npz_file_name(j, i)
                    mtx_a = load_lil(file_a)
                    mtx_b = load_lil(file_b)
                    a_xor_b, a_union_b, a_to_b, b_to_a = calc_enc_bet_mtx(mtx_a, mtx_b)
                    calculated_list.append((i, j))
                    calculated_list.append((j, i))
                    row_1 = [str(i) + '->' + str(j), a_xor_b, a_union_b, a_to_b, b_to_a]
                    row_2 = [str(j) + '->' + str(i), a_xor_b, a_union_b, b_to_a, a_to_b]
                    with open('EncountersInfo.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(row_1)
                        writer.writerow(row_2)
                        print(row_1)
                        print(row_2)


def run_diff_per_days_for_all_pairs(personal_list, calc_list):
    calculated_list = calc_list
    for i in personal_list:
        for j in personal_list:
            if i != j:
                if (i, j) not in calculated_list:
                    file_a = get_npz_file_name(i, j)
                    file_b = get_npz_file_name(j, i)
                    mtx_a = load_lil(file_a)
                    mtx_b = load_lil(file_b)
                    days_agreement_dictionary_a_to_b = calc_enc_bet_mtx_for_diff_of_days(mtx_a, mtx_b, 190)
                    mtx_a = load_lil(file_a)
                    mtx_b = load_lil(file_b)
                    days_agreement_dictionary_b_to_a = calc_enc_bet_mtx_for_diff_of_days(mtx_b, mtx_a, 190)
                    calculated_list.append((i, j))
                    calculated_list.append((j, i))
                    # row_1 = [str(i) + '->' + str(j)]
                    row_2 = [str(i) + '->' + str(j)]
                    row_temp = []
                    row_3 = []
                    for key, value in days_agreement_dictionary_b_to_a.items():
                        row_temp.append(value)
                    row_temp.reverse()
                    row_mid = row_2 + row_temp
                    for key, value in days_agreement_dictionary_a_to_b.items():
                        # row_1.append(key)
                        row_3.append(value)
                    row = row_mid + row_3
                    with open('exmp.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        # writer.writerow(row_1)
                        writer.writerow(row)
                        # print(row_1)
                        print(row)


def calc_enc_bet_mtx_for_diff_of_days(mtx_a, mtx_b, days_count):
    """
    calculate agreement for the the given values of
    days between to lines of sparse matrix.
    :param mtx_a:
    :param mtx_b:
    :param days_count:
    :return:
    """
    diff_per_days = {}
    a_xor_b = 0
    a_union_b = 0
    non_zero_a_list = mtx_a.nonzero()[1]
    non_zero_b_list = mtx_b.nonzero()[1]
    non_zero_a = set(non_zero_a_list)
    non_zero_b = set(non_zero_b_list)

    for i in range(days_count):

        for value_a in non_zero_a:
            a_union_b += 1
            value = value_a + i
            if value in non_zero_b:
                a_xor_b += 1
        for value_b in non_zero_b:
            value = value_b - i
            if value not in non_zero_a:
                a_union_b += 1
        if a_union_b == 0:
            diff_per_days[i] = 0
        else:
            diff_per_days[i] = a_xor_b / a_union_b

    return diff_per_days


def write_head_line():
    pair, a_xor_b, a_union_b, a_to_b, b_to_a = 'Pair: a-b', 'a_xor_b', 'a_union_b', 'a_to_b', 'b_to_a'
    head_line = [pair, a_xor_b, a_union_b, a_to_b, b_to_a]
    with open('EncountersInfo.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(head_line)


def save_lil(filename, mtx):
    np.savez(filename, dtype=mtx.dtype.str, data=mtx.data, rows=mtx.rows, shape=mtx.shape)


def load_lil(filename):
    loader = np.load(filename)
    result = lil_matrix(tuple(loader["shape"]), dtype=str(loader["dtype"]))
    result.data = loader["data"]
    result.rows = loader["rows"]
    return result


def count_total_encounters_for_pair(personal_list, calc_list):
    calculated_list = calc_list
    for i in personal_list:
        for j in personal_list:
            if i != j:
                if (i, j) not in calculated_list:
                    file_a = get_npz_file_name(i, j)
                    file_b = get_npz_file_name(j, i)
                    mtx_a = load_lil(file_a)
                    mtx_b = load_lil(file_b)
                    count_a_to_b = mtx_a.count_nonzero()
                    count_b_to_a = mtx_b.count_nonzero()
                    total = count_a_to_b + count_b_to_a
                    calculated_list.append((i, j))
                    calculated_list.append((j, i))
                    row_1 = [str(i) + '<->' + str(j)]
                    row_1.append(count_a_to_b)
                    row_1.append(count_b_to_a)
                    row_1.append(total)
                    with open('Count_per_pair.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(row_1)
                        # writer.writerow(row_2)
                        print(row_1)
                        # print(row_2)


def read_encounters_count():
    dict = {}
    with open('Count_per_pair.csv', mode='r') as f:
        reader = csv.DictReader(f)
        for rows in reader:
            key = parse_symetric_pair_to_tuple(rows['pair'])
            total = rows['total']
            dict[key] = int(total)

    return dict


def find_offset_to_maximize_agreement():
    dict = {}
    with open('AgreementForDayDiff190.csv', mode='r') as f:
        reader = csv.reader(f)
        my_list = list(reader)
        offset_list = my_list[0]
        for ls in my_list[1:]:
            value = max(ls[1:])
            if value == '0':
                offset = 'null'
            else:
                index = ls.index(value)
                offset = index - 190
            # print(offset)
            pair = parse_asymetric_pair_to_tuple(ls[0])
            dict[pair] = offset
    # print(dict)
    return dict


def parse_symetric_pair_to_tuple(key):
    spl = key.split('<->')
    tup = (spl[0], spl[1])
    return tup


def parse_asymetric_pair_to_tuple(key):
    spl = key.split('->')
    tup = (spl[0], spl[1])
    return tup


def fix_offset(offset_dic, encounters_count_dic):

    for key, value in offset_dic.items():

        if value != 'null':
            if not os.path.isfile('LIL_mtx_new//LIL[' + str(key[0]) + "-" + str(key[1]) + '].npz'):

                file_a = get_npz_file_name(key[0], key[1])
                file_b = get_npz_file_name(key[1], key[0])
                mtx_a = load_lil(file_a)
                mtx_b = load_lil(file_b)
                if mtx_a.count_nonzero() > 15:
                    a = mtx_a.nonzero()[1]

                    for v in a:
                        mtx_a[[0], [v]] = 0
                        col = v + offset_dic[key]
                        if col < 5270400:
                            mtx_a[[0], [col]] = 1
                        # 'LIL_mtx_new//LIL[' + str(key[0]) + "-" + str(key[1]) + '].npz'
                    save_lil('LIL_mtx_new//LIL[' + str(key[0]) + "-" + str(key[1]) + '].npz', mtx_a)
                    save_lil('LIL_mtx_new//LIL[' + str(key[1]) + "-" + str(key[0]) + '].npz', mtx_b)


# i don't remember why i used exmp func"
def exmp(personal_list, calc_list):
    calculated_list = calc_list
    for i in personal_list:
        for j in personal_list:
            if i != j:
                if (i, j) not in calculated_list:
                    file_a = get_npz_file_name(i, j)
                    file_b = get_npz_file_name(j, i)
                    mtx_a = load_lil(file_a)
                    mtx_b = load_lil(file_b)
                    a_xor_b, a_union_b, a_to_b, b_to_a = calc_enc_bet_mtx(mtx_a, mtx_a)
                    calculated_list.append((i, j))
                    calculated_list.append((j, i))
                    row_1 = [str(i) + '->' + str(j), a_xor_b, a_union_b, a_to_b, b_to_a]
                    row_2 = [str(j) + '->' + str(i), a_xor_b, a_union_b, b_to_a, a_to_b]
                    with open('Exmp.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(row_1)
                        writer.writerow(row_2)
                        print(row_1)
                        print(row_2)


def initialize_specific_range():
    days = []
    start_date = datetime.date(2017, 6, 13)
    end_date = datetime.date(2017, 8, 13)
    dates = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date-start_date).days)]

    for date in dates:
        day_range = determine_day_range(date)
        new_day = Date(date, day_range)
        days.append(new_day)
    return days


def determine_day_range(date):
    # night_range = []
    ein_gedi = ephem.Observer()
    ein_gedi.date = ephem.Date(date)
    ein_gedi.lat = '31.46720101'
    ein_gedi.lon = '35.39643957'
    end_time = ein_gedi.next_setting(ephem.Sun()).datetime()
    end_time = end_time + datetime.timedelta(hours=3)
    start_time = ein_gedi.next_rising(ephem.Sun()).datetime()
    start_time = start_time + datetime.timedelta(hours=3)

    day_range = [start_time + datetime.timedelta(seconds=x) for x in range(0, (end_time-start_time).seconds)]

    return day_range


def determine_time(second):
    # day = second // (24 * 3600)
    second = second % (24 * 3600)
    hour = second // 3600
    second %= 3600
    minutes = second // 60
    second %= 60
    seconds = second
    return datetime.time(hour, minutes, seconds)


def get_time_of_day(dates, second):
    night = 0
    # day, sec_found = find_time(days, second)
    day = int(second/length_of_day)
    date = dates[day]
    spec_time = determine_time(second)
    date_time = datetime.datetime.combine(date.date, spec_time)

    day_range = date.day_range

    start_time = day_range[0]
    end_time = day_range[-1]
    if start_time < date_time < end_time:
        night = 0
    else:
        night = 1

    return date.date, spec_time, night


class Date:
    def __init__(self, date, day_range):
        self.date = date
        self.day_range = day_range








