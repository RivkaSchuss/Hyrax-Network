import ParseDetails as pd
import HelperMethods as h
import csv
import datetime
import os
import pandas as pan
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO
from IPython.display import Image
import pydotplus

day_meet_count = 100
night_meet_count = 100

total_days_range = 60

start_date = datetime.date(2017, 6, 13)
list_prefix = 'count-per-days-pairs/count_per_{}_for_{}-{}.txt'
db_global_name = 'DB/data_{}.csv'.format(datetime.datetime.now().strftime("%H%M_%S%f_%B_%d_%Y"))


def learn(h_list):
    days_cluster_list, night_cluster_list = get_cluster_per_day(h_list, min_meeting_length=20)


def train(h_list, last_n_list_param, should_make_graph=True):
    col_names = ["Hyrax", "Partner"]
    feature_cols = ["Sex"]
    for n in last_n_list_param:
        feature_cols.extend([str(n) + '_day_meet_count', str(n) + '_night_meet_count'])
    col_names.extend(feature_cols)
    col_names.append("Did_meet_night_later")
    pima = pan.read_csv(db_global_name, header=None, names=col_names)
    x = pima[feature_cols]
    y = pima.Did_meet_night_later

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)

    clf = DecisionTreeClassifier("entropy", max_depth=4)
    clf = clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)
    print(last_n_list_param)
    acc = metrics.accuracy_score(y_test, y_pred)
    print("Accuracy:", acc)

    if should_make_graph:
        dot_data = StringIO()
        export_graphviz(clf, out_file=dot_data,
                        filled=True, rounded=True,
                        special_characters=True, feature_names=feature_cols, class_names=['False', 'True'])
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_png('tree.png')
        Image(graph.create_png())
    return acc


def make_db_for_tree(h_list, last_n_list_param):
    db_name = db_global_name
    hyrax_dict, basestation_dict, start, end = pd.parse_details()

    calc_list = []
    for i in h_list:
        calc_list.append(i)
        hy_dict = {"hyrax": i}
        if hyrax_dict[i].sex == 'M':
            hy_dict['Sex'] = 1
        else:
            hy_dict['Sex'] = 0
        for j in h_list:
            if i != j:
                with open(list_prefix.format('day', i, j), 'r') as file:
                    day_list = eval(file.readline())

                with open(list_prefix.format('night', i, j), 'r') as file:
                    night_list = eval(file.readline())

                with open(db_name, 'a', newline='') as outcsv:
                    for d in range(total_days_range):
                        last_n_list = []
                        for n in last_n_list_param:
                            last_n_days, last_n_nights = get_last_n_days(day_list, night_list, n, d)
                            last_n_list.append((last_n_days, last_n_nights))
                        if night_list[d + 1] > night_meet_count:
                            next_night = True
                        else:
                            next_night = False
                        if check_if_one_is_zero(last_n_list):
                            continue
                        row = [i, j, hy_dict['Sex']]
                        for last in last_n_list:
                            row.extend([last[0], last[1]])
                        row.append(next_night)
                        writer = csv.writer(outcsv)
                        writer.writerow(row)


def check_if_one_is_zero(last_n_list):
    for last in last_n_list:
        if last[0] == 0 and last[1] == 0:
            return True
    return False


def get_last_n_days(day_list, night_list, n, index):
    last_n_day = 0
    last_n_night = 0
    for i in range(n):
        if index - i > 0:
            last_n_day += day_list[index - i]
            last_n_night += night_list[index - i]
    return last_n_day, last_n_night


def save_count_per_day_to_file(h_list, hyrax_dict):
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

                save_list(list_prefix.format('day', str(i), str(j)), days_count)
                save_list(list_prefix.format('night', str(i), str(j)), night_count)


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
