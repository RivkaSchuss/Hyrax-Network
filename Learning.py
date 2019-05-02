import ParseDetails as pd
import HelperMethods as h
import csv
import datetime
import os
import pandas as pan
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics


day_meet_count = 100
night_meet_count = 100

start_date = datetime.date(2017, 6, 13)
list_prefix = 'count-per-days-pairs/count_per_{}_for_{}-{}.txt'


def learn(h_list):
    days_cluster_list, night_cluster_list = get_cluster_per_day(h_list, min_meeting_length=20)


def train(h_list):

    col_names = ["Hyrax", "Partner", "1_day_meet_count", "1_night_meet_count", "Sex", "Did_meet_night_later"]
    pima = pan.read_csv('DB/dataSet.csv', header=None, names=col_names)
    feture_cols = ["1_day_meet_count", "1_night_meet_count", "Did_meet_night_later"]
    x = pima[feture_cols]
    y = pima.Did_meet_night_later

    x_train, x_test, y_train,y_test = train_test_split(x, y, test_size=0.9, random_state=1)

    clf = DecisionTreeClassifier()
    clf = clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    # days_cluster_list, night_cluster_list = get_cluster_per_day(hyrax_dict)

    # make_db_for_tree(h_list)


def make_db_for_tree(h_list):
    hyrax_dict, basestation_dict, start, end = pd.parse_details()

    # days_cluster_list, night_cluster_list = get_cluster_per_day(h_list, min_meeting_length=20)

    for i in h_list:

        hy_dict = {}
        hy_dict["hyrax"] = i
        hy_dict['Sex'] = hyrax_dict[i].sex
        for j in h_list:
            if i != j:
                day_list = []
                night_list = []
                last_day = 'not_assigned'
                last_night = 'not_assigned'
                next_night = 'not_assigned'
                with open(list_prefix.format('day', i, j), 'r') as file:
                    day_list = eval(file.readline())

                with open(list_prefix.format('night', i, j), 'r') as file:
                    night_list = eval(file.readline())

                with open('DB/dataSet.csv', 'a', newline='') as outcsv:
                    for d in range(60):
                        last_day = day_list[d]
                        last_night = night_list[d]
                        if night_list[d+1] > night_meet_count:
                            next_night = True
                        else:
                            next_night = False

                        writer = csv.writer(outcsv)
                        writer.writerow([i, j, last_day, last_night, hy_dict['Sex'], next_night])


def save_count_per_day_to_file(h_list, hyrax_dict):
    # days = h.initialize_days()
    date_times = h.initialize_specific_range()

    for i in h_list:

        for j in h_list:
            if i != j:
                if os.path.isfile(list_prefix.format('day', str(i), str(j))):
                    continue
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
                # list_prefix = 'count-per-days-pairs/count_per_{}_for_{}-{}.txt'

                save_list(list_prefix.format('day', str(i), str(j)), days_count)
                save_list(list_prefix.format('night', str(i), str(j)), night_count)
                # print("here")


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
    # night_clusters = create_clusters(nights, min_meeting_length, date_times)

    return day_clusters, #night_clusters


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
                        clusters[date][meeting.j] = i_cluster_val
                    elif j_cluster_val is not None and i_cluster_val is None:
                        clusters[date][meeting.i] = j_cluster_val
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

