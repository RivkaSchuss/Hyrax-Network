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


print personal_list
# mtx = lil_matrix((484, 5270400))
# mtx[0, 0] = 1

# print mtx
