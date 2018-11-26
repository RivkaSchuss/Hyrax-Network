import datetime
import ParseDetails
import HelperMethods
from scipy.sparse import lil_matrix

# import

hyrax_dict, base_station_dict, last_on, first_off = ParseDetails.parse_details()

# print last_on

encounters_list = HelperMethods.add_all_encounters(hyrax_dict, last_on, first_off)

# HelperMethods.print_in_intervals(encounters_list)

personal_list = []

for i in encounters_list:
    id = i.get_personal_id()
    if not personal_list.__contains__(id):
        personal_list.append(id)

# print personal_list
pair_to_row_dict = HelperMethods.assign_pairs_to_dict(personal_list)

start_experiment_date = datetime.datetime(2017, 6, 13, 00, 00)
exp_date = encounters_list[3].get_full_date()
print exp_date
exp_length = encounters_list[3].get_length()
# exp_date = datetime.datetime(2017, 6, 14, 00, 01)
i, j = HelperMethods.get_columns_indexes_by_time(start_experiment_date, exp_date, exp_length)
print i
print j

print HelperMethods.get_time_from_column_index(start_experiment_date, i)
print HelperMethods.get_time_from_column_index(start_experiment_date, j)

# HelperMethods.get_columns_indexes_by_time(encounters_list.__getitem__(2).)
mtx = lil_matrix((484, 5270400))

# print mtx
