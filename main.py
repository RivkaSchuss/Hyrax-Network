import datetime
import ParseDetails
import HelperMethods

hyrax_dict, base_station_dict, last_on, first_off = ParseDetails.parse_details()

print last_on

encounters_list = HelperMethods.add_all_encounters(hyrax_dict, last_on, first_off)

for i in range(24):
    s = datetime.time(i % 24, 00)
    t = datetime.time((i + 1) % 24, 00)
    count = HelperMethods.get_by_hours(encounters_list, s, t)
    print "Between " + str(i) + ":00  to " + str((i + 1)) + ":00 - " + str(count)
    # print count

