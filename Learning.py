import ParseDetails as pd
import HelperMethods as h
import csv
import datetime

day_meet_count = 100
night_meet_count = 100

start_date = datetime.date(2017, 6, 13)


def learn(h_list):
    hyrax_dict, basestation_dict, start, end = pd.parse_details()

    days_cluster_list, night_cluster_list = get_cluster_per_day(h_list, min_meeting_length=20)


    save_count_per_day_to_file(h_list, hyrax_dict)

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


def save_count_per_day_to_file(h_list, hyrax_dict):
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


def get_cluster_per_day(h_list, min_meeting_length):
    days = dict()
    nights = dict()
    date_times = h.initialize_specific_range()
    for date in date_times:
        days[date] = list()
        nights[date] = list()
    for i in h_list:
        for j in h_list:
            if i != j:
                mtx_a = h.load_lil(h.get_npz_file_name(i, j))
                non_zero = mtx_a.nonzero()[1]
                current_date = None
                meeting_counter = 0
                for v in non_zero:
                    date, time, night = h.get_time_of_day(date_times, v)
                    if meeting_counter == 0:
                        current_date = date
                    if current_date is not date:
                        if night == 1:
                            nights[current_date].append(Meeting(i, j, meeting_counter))
                        else:
                            days[current_date].append(Meeting(i, j, meeting_counter))
                        meeting_counter = 0
                        continue
                    else:
                        meeting_counter += 1

    day_clusters = create_clusters(days, min_meeting_length, date_times)
    night_clusters = create_clusters(nights, min_meeting_length, date_times)

    return day_clusters, night_clusters


def create_clusters(dic_dates, min_meeting_length, date_times):
    clusters = dict()
    for date in date_times:
        clusters[date] = dict()
    for date, meetings in dic_dates.items():
        cluster_count_day = 1
        for meeting in meetings:
            length = meeting.length
            if length >= min_meeting_length:
                if len(clusters[date]) == 0:
                    clusters[date][meeting.j] = cluster_count_day
                    clusters[date][meeting.i] = cluster_count_day
                else:
                    i_cluster_val = clusters[date].get(meeting.i)
                    j_cluster_val = clusters[date].get(meeting.j)
                    if i_cluster_val is None and j_cluster_val is None:
                        cluster_count_day += 1
                        clusters[date][meeting.j] = cluster_count_day
                        clusters[date][meeting.i] = cluster_count_day
                    elif i_cluster_val is not None and j_cluster_val is None:
                        cluster_count_day += 1
                        clusters[date][meeting.j] = cluster_count_day
                        clusters[date][meeting.i] = i_cluster_val
                    elif j_cluster_val is not None and i_cluster_val is None:
                        cluster_count_day += 1
                        clusters[date][meeting.i] = cluster_count_day
                        clusters[date][meeting.j] = j_cluster_val
                    else:
                        clusters[date][meeting.i] = i_cluster_val
                        clusters[date][meeting.j] = j_cluster_val
    return clusters


def save_list(list_name, list_var):
    with open(list_name, "w") as file:
        file.write(str(list_var))


class Meeting:
    def __init__(self, i, j, length):
        self.i = i
        self.j = j
        self.length = length

