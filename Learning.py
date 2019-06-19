import ParseDetails as pd
import HelperMethods as h
import csv
import datetime
import os
import pandas as pan
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO
from IPython.display import Image
import pydotplus

# hyper parameters:
day_meet_count = 100
predict_meet_count = 900
tree_depth = 3

start_hour_range = 5
end_hour_range = 18

total_days_range = 60

different_sex_value = -1
female_value = 0
male_value = 1

same_canyon = 1
different_canyon = 0

same_group = 1
different_group = 0
one_is_bachelor = -1
both_bachelors = -2

start_date = datetime.date(2017, 6, 13)
list_prefix = 'count-per-days-pairs/count_per_{}_for_{}-{}.txt'
db_global_name = 'DB/data_{}.csv'.format(datetime.datetime.now().strftime("%H%M_%S%f_%B_%d_%Y"))
db_hours_global_name = 'DB/data_hours_{}.csv'.format(datetime.datetime.now().strftime("%H%M_%S%f_%B_%d_%Y"))
list_hours_prefix = 'count-per-hours-pairs/count_hour_for_{}-{}.txt'


def make_db_and_train_by_hours(h_list, should_make_graph=True):
    make_db_by_hours(h_list)
    hours_train(should_make_graph)


def make_db_by_hours(h_list):
    db_name = db_hours_global_name
    calc_list = []
    for i in h_list:
        calc_list.append(i)
        for j in h_list:
            if i != j:

                with open(list_hours_prefix.format(i, j), 'r') as file:
                    hour_list = eval(file.readline())

                with open(list_prefix.format('night', i, j), 'r') as file:
                    night_list = eval(file.readline())

                with open(db_name, 'a', newline='') as outcsv:
                    for d in range(total_days_range):
                        flag = False
                        for z in hour_list[d][start_hour_range:end_hour_range]:
                            if z != 0:
                                flag = True
                                break
                        if flag is False:
                            continue
                        row = [i, j]
                        row.extend(hour_list[d][start_hour_range:end_hour_range])
                        if night_list[d + 1] > predict_meet_count:
                            next_night = True
                        else:
                            next_night = False
                        row.append(next_night)
                        writer = csv.writer(outcsv)
                        writer.writerow(row)


def hours_train(should_make_graph):
    col_names = ["Hyrax", "Partner"]
    feature_cols = []

    for n in range(start_hour_range, end_hour_range):
        feature_cols.extend([str(n) + '_hour_meet_count'])

    col_names.extend(feature_cols)
    col_names.append("Did_meet_night_later")
    pima = pan.read_csv(db_hours_global_name, header=None, names=col_names)
    x = pima[feature_cols]
    y = pima.Did_meet_night_later

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

    clf = DecisionTreeClassifier("entropy", max_depth=tree_depth)
    clf = clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)
    print(feature_cols)
    acc = metrics.accuracy_score(y_test, y_pred)
    print("Accuracy:", acc)

    print("F_Score: " + str(metrics.f1_score(y_test, y_pred, average='weighted')))

    print("Recall: " + str(metrics.recall_score(y_test, y_pred, average='weighted')))

    print("Precision: " + str(metrics.precision_score(y_test, y_pred, average='weighted')))

    reg = DecisionTreeRegressor(max_depth=tree_depth, criterion="mse")
    reg.fit(x_train, y_train)
    # y_pred can be used to give likelihood to meet the next day
    y_pred = reg.predict(x_test)

    score = reg.score(x_train, y_train)
    print("Regression Score:", score)

    if should_make_graph:
        dot_data = StringIO()
        export_graphviz(clf, out_file=dot_data,
                        filled=True, rounded=True,
                        special_characters=True, feature_names=feature_cols, class_names=['False', 'True'])
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_png('tree.png')
        Image(graph.create_png())
    return acc


def make_db_and_train(h_list, last_n_list=None, sex=False, should_make_graph=True, group=False, canyon=False):
    make_db_for_tree(h_list, last_n_list_param=last_n_list, sex=sex, group=group, canyon=canyon)
    train(last_n_list_param=last_n_list, sex=sex, group=group, canyon=canyon,
          should_make_graph=should_make_graph)


def train(last_n_list_param=None, sex=False, group=False, canyon=False, should_make_graph=True):
    col_names = ["Hyrax", "Partner"]
    feature_cols = []
    if sex:
        feature_cols.append("Sex")
    if group:
        feature_cols.append("Group")
    if canyon:
        feature_cols.append("Canyon")

    if last_n_list_param is not None:
        for n in last_n_list_param:
            feature_cols.extend([str(n) + '_day_meet_count', str(n) + '_night_meet_count'])

    if last_n_list_param == 'hours':
        print('hours')

    col_names.extend(feature_cols)
    col_names.append("Did_meet_night_later")
    pima = pan.read_csv(db_global_name, header=None, names=col_names)
    x = pima[feature_cols]
    y = pima.Did_meet_night_later

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

    clf = DecisionTreeClassifier("entropy", max_depth=tree_depth)
    clf = clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)
    print(feature_cols)
    acc = metrics.accuracy_score(y_test, y_pred)
    print("Accuracy:", acc)

    print("F_Score: " + str(metrics.f1_score(y_pred, y_test, average='weighted')))

    print("Recall: " + str(metrics.recall_score(y_test, y_pred, average='weighted')))

    print("Precision: " + str(metrics.precision_score(y_test, y_pred, average='weighted')))

    reg = DecisionTreeRegressor(max_depth=tree_depth, criterion="mse")
    reg.fit(x_train, y_train)
    # y_pred can be used to give likelihood to meet the next day
    y_pred = reg.predict(x_test)

    score = reg.score(x_train, y_train)
    print("Regression Score:", score)

    if should_make_graph:
        dot_data = StringIO()
        export_graphviz(clf, out_file=dot_data,
                        filled=True, rounded=True,
                        special_characters=True, feature_names=feature_cols, class_names=['False', 'True'])
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_png('tree.png')
        Image(graph.create_png())
    return acc


def make_db_for_tree(h_list, last_n_list_param=None, sex=False, group=False, canyon=False, predict_night=False):
    db_name = db_global_name
    hyrax_dict, basestation_dict, start, end = pd.parse_details()

    calc_list = []
    for i in h_list:
        calc_list.append(i)
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

                        if predict_night:
                            predict_list = night_list[d + 1]
                        else:
                            predict_list = day_list[d + 1]

                        if predict_list > predict_meet_count:
                            predict = True
                        else:
                            predict = False
                        if check_if_one_is_zero(last_n_list):
                            continue

                        row = [i, j]
                        if sex:
                            row.append(assign_sex_value(hyrax_dict[i].sex, hyrax_dict[j].sex))
                        if group:
                            row.append(assign_group_value(hyrax_dict[i].group, hyrax_dict[j].group))
                        if canyon:
                            row.append(assign_canyon_value(hyrax_dict[i].canyon, hyrax_dict[j].canyon))
                        for last in last_n_list:
                            row.extend([last[0], last[1]])
                        row.append(predict)
                        writer = csv.writer(outcsv)
                        writer.writerow(row)


def make_histogram(h_list, is_night=False, diff=100, min_value=10, csv_name="histogram.csv"):
    max_value = min_value + diff
    calc_list = []
    intervals = int((8 * 3600) / diff) - 100
    interval_dict = {}
    for interval in range(intervals):

        total = 0
        size = interval * diff
        for i in h_list:
            calc_list.append(i)

            for j in h_list:
                if i != j:
                    if is_night:
                        with open(list_prefix.format('night', i, j), 'r') as file:
                            list_to_insert = eval(file.readline())
                    else:
                        with open(list_prefix.format('day', i, j), 'r') as file:
                            list_to_insert = eval(file.readline())

                    for time_interval in list_to_insert:
                        if (max_value + size) > time_interval > (min_value + size):
                            total += 1
        interval_dict[interval, min_value + size, max_value + size] = total
    with open(csv_name, 'w') as file:
        file.write("%s,%s,%s\n" % ("Iter", "min_value", "max_value"))
        for key, value in interval_dict.items():
            file.write("%s,%s,%s,%s\n" % (key[0], key[1], key[2], value))

    print(interval_dict)


def assign_canyon_value(i_canyon, j_canyon):
    if i_canyon == j_canyon:
        return same_canyon
    else:
        return different_canyon


def assign_group_value(i_group, j_group):
    if i_group == 'Bachelor' and j_group == 'Bachelor':
        return both_bachelors
    if i_group == 'Bachelor' or j_group == 'Bachelor':
        return one_is_bachelor
    if i_group == j_group:
        return same_group
    if i_group != j_group:
        return different_group
    else:
        raise Exception("Error in group assignment")


def assign_sex_value(i_sex, j_sex):
    sex_value = -100
    if i_sex != j_sex:
        sex_value = different_sex_value
    elif i_sex == 'M':
        sex_value = male_value
    elif i_sex == 'F':
        sex_value = male_value
    if sex_value == -100:
        raise Exception("Error in sex assignment")
    return sex_value


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


def save_count_per_hour_to_file(h_list):
    date_times = h.initialize_specific_range()
    for i in h_list:
        for j in h_list:
            if i != j:
                if os.path.isfile(list_hours_prefix.format(i, j)):
                    continue
                days_count = []
                for e in range(61):
                    days_count.append([0] * 24)
                # days_count = [[0] * 24] * 61
                # days_count[2][4] = 5
                mtx_a = h.load_lil(h.get_npz_file_name(i, j))
                non_zero = mtx_a.nonzero()[1]
                for v in non_zero:
                    date, time, night = h.get_time_of_day(date_times, v)
                    delta_days = date - start_date
                    days_count[delta_days.days][time.hour] += 1
                save_list(list_hours_prefix.format(i, j), days_count)


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


def save_list(list_name, list_var):
    with open(list_name, "w") as file:
        file.write(str(list_var))


def eval_list(list_name):
    with open(list_name, "r") as file:
        s = file.read()
        list = eval(s)

    return list


class Meeting:
    def __init__(self, i, j, length):
        self.i = i
        self.j = j
        self.length = length
