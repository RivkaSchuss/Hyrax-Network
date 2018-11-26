import ICollar
import datetime

import math


def add_all_encounters(hyrax_dict, start_date, end_date):
    encounter_list = []
    for key, hyrax in hyrax_dict.iteritems():
        hyrax.filter_encounters(start_date, end_date)
        filtered_dict = hyrax.get_filtered_encounters()
        for id, encounter in filtered_dict.iteritems():
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
        print "Between " + str(i) + ":00  to " + str((i + 1)) + ":00 - " + str(count)


def assign_pairs_to_dict(personal_list):
    pair_to_row_dict = {}
    row_count = 0
    for p_id in personal_list:
        count = len(personal_list)
        for i in range(count):
            if p_id != personal_list[i]:
                row_name = str(p_id) + "," + str(personal_list[i])
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

