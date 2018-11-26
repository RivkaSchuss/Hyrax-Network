import datetime
import ParseDetails
import HelperMethods
from scipy.sparse import lil_matrix


start_experiment_date = datetime.datetime(2017, 6, 13, 00, 00)
hyrax_dict, base_station_dict, last_on, first_off = ParseDetails.parse_details()

encounters_list = HelperMethods.add_all_encounters(hyrax_dict, last_on, first_off)

personal_list = []

for i in encounters_list:
    id = i.get_personal_id()
    if not personal_list.__contains__(id):
        personal_list.append(id)

pair_to_row_dict = HelperMethods.assign_pairs_to_dict(personal_list)

# mtx = lil_matrix((484, 5270400))

