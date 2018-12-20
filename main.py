import datetime
import ParseDetails
import HelperMethods
from scipy.sparse import lil_matrix
from scipy import sparse
import numpy as np
import json

start_experiment_date = datetime.datetime(2017, 6, 13, 00, 00)
hyrax_dict, base_station_dict, last_on, first_off = ParseDetails.parse_details()

def main():
    start_experiment_date = datetime.datetime(2017, 6, 13, 00, 00)
    hyrax_dict, base_station_dict, last_on, first_off = ParseDetails.parse_details()

    encounters_list = HelperMethods.add_all_encounters(hyrax_dict, last_on, first_off)

    personal_list = []

    for i in encounters_list:
        id = i.get_personal_id()
        if not personal_list.__contains__(id):
            personal_list.append(id)

# print(personal_list)
pair_to_row_dict = HelperMethods.assign_pairs_to_dict(personal_list)
print(pair_to_row_dict)
mtx = lil_matrix((484, 5270400))

for e in encounters_list:
    if e.personal_id in personal_list and int(e.enc_id) in personal_list:
        i, j = HelperMethods.get_columns_indexes_by_time(start_experiment_date, e.full_date, e.length)
        personal = e.personal_id
        other_hyrax = int(e.enc_id)
        t = tuple([e.personal_id, other_hyrax])
        row = pair_to_row_dict[t]
        HelperMethods.add_values_to_lil(mtx, row, i, j)



    mtx = lil_matrix((20, 20))
    for i in range(20):
        HelperMethods.add_values_to_lil(mtx, i, 4, 8)

    filename = 'LIL.npz'

    save_lil(filename, mtx)
    loaded_mtx = load_lil(filename)
    print(loaded_mtx)


def save_lil(filename, mtx):
    np.savez(filename, dtype=mtx.dtype.str, data=mtx.data, rows=mtx.rows, shape=mtx.shape)


def load_lil(filename):
    loader = np.load(filename)
    result = lil_matrix(tuple(loader["shape"]), dtype=str(loader["dtype"]))
    result.data = loader["data"]
    result.rows = loader["rows"]
    return result


if __name__ == '__main__':
    main()







