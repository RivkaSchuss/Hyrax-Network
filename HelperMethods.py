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
    for e in encounter_list:
        # print e.full_date
        # print e.full_date.time()
        if start < e.full_date.time() < end:
            if time_interval_min < e.length < time_interval_max:
                count += 1

    return count
