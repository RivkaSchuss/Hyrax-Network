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


def get_cluster_per_day(hyrax_dict):
    days = []
    nights = []
    return days, nights


def save_list(list_name, list_var):
    with open(list_name, "a") as file:
        file.write(str(list_var))
