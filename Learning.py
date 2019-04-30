import ParseDetails as pd
import HelperMethods as h
import csv
import datetime

day_meet_count = 100
night_meet_count = 100

start_date = datetime.date(2017, 6, 13)


def learn(h_list):

    save_count_per_day_to_file(h_list)

    # hyrax_dict, basestation_dict, start, end = pd.parse_details()
    #
    # days = h.initialize_days()
    # date_times = h.initialize_specific_range()
    # date, time, night = h.get_time_of_day(days, date_times, 3)
    # print(date, time, night)
    # with open('dataSet.csv', 'a') as outcsv:
    #     writer = csv.writer(outcsv)
    #     writer.writerow(["a", "b", "c", "d", "e"])
    #     writer.writerow(["hyrax", "pair", "1_day_meet_count", "1_night_meet_count", "Sex", "did_meet"])

    # print(i)
                # mtx_b = h.load_lil(h.get_npz_file_name(j, i))

        # print(hyrax_dict[hy].sex)


def save_count_per_day_to_file(h_list):
    hyrax_dict, basestation_dict, start, end = pd.parse_details()

    # days = h.initialize_days()
    date_times = h.initialize_specific_range()

    for i in h_list:
        hy_dict = {}
        hy_dict["hyrax"] = i
        hy_dict['Sex'] = hyrax_dict[i].sex
        for j in h_list:
            if i != j:
                days_count = [0] * 61
                night_count = [0] * 61
                mtx_a = h.load_lil(h.get_npz_file_name(i, j))
                non_zero = mtx_a.nonzero()[1]

                for v in non_zero:
                    date, time, night = h.get_time_of_day(date_times, v)
                    delta = date - start_date
                    if night == 1:
                        night_count[delta.days] += 1
                    else:
                        days_count[delta.days] += 1



def save_list(list_name, list_var):

    with open(list_name, "w") as file:
        file.write(str(list_var))
