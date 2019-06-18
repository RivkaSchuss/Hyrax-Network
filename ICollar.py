import datetime


class ICollar:

    def __init__(self, collar_id):
        self.collar_id = collar_id
        self.encounters = dict()
        self.filtered_encounters = dict()

    def add_encounter(self, enc_id, encounter):
        self.encounters[enc_id] = encounter

    def filter_encounters(self, start_date, last_date):
        for enc_id, encounter in self.encounters.items():
            if start_date < encounter.date < last_date:
                self.filtered_encounters[enc_id] = encounter

    def get_filtered_encounters(self):
        return self.filtered_encounters


class Hyrax(ICollar):
    def __init__(self, collar_id, serial_number=None, chip=None, tag=None, old_collar=None, canyon=None,
                 group=None, sex=None, weight=None, date_on=None, date_off=None,
                 seconds_off=None, daily_offset=None, data_points=None, comments=None):
        ICollar.__init__(self, collar_id)
        self.collar_id = collar_id
        self.serial_number = serial_number
        self.chip = chip
        self.tag = tag
        self.old_collar = old_collar
        self.canyon = canyon
        self.group = group
        self.sex = sex
        self.weight = weight
        self.date_on = date_on.split("/")
        self.date_off = date_off.split("/")
        self.seconds_off = seconds_off
        self.daily_offset = daily_offset
        self.data_points = data_points
        self.comments = comments

    def set_value(self, array, i):
        try:
            value = array[i]
        except IndexError:
            value = ""
        return value

    def __init__(self, collar_id, array, real_data_folder_path):
        ICollar.__init__(self, collar_id)
        i = 0
        self.collar_id = self.set_value(array, i)
        i += 1
        self.serial_number = self.set_value(array, i)
        i += 1
        self.chip = self.set_value(array, i)
        i += 1
        self.tag = self.set_value(array, i)
        i += 1
        self.old_collar = self.set_value(array, i)
        i += 1
        self.canyon = self.set_value(array, i)
        i += 1
        self.group = self.set_value(array, i)
        i += 1
        self.sex = self.set_value(array, i)
        i += 1
        self.weight = self.set_value(array, i)
        i += 1
        self.date_on = self.set_value(array, i).split(" ")
        i += 1
        self.date_off = self.set_value(array, i).split(" ")
        i += 1
        self.seconds_off = self.set_value(array, i)
        i += 1
        self.daily_offset = self.set_value(array, i)
        i += 1
        self.data_points = self.set_value(array, i)
        i += 1
        self.comments = self.set_value(array, i)
        i += 1
        self.real_data_path = self.set_real_data_path(real_data_folder_path)

    def set_real_data_path(self, real_data_folder_path):
        return real_data_folder_path + "/logger" + self.collar_id + "_" + self.tag + ".csv"

    def get_real_data_path(self):
        return self.real_data_path

    def get_hyrax_id(self):
        return self.collar_id

    def get_serial_number(self):
        return self.serial_number

    def get_chip(self):
        return self.chip

    def get_tag(self):
        return self.tag

    def get_old_collar(self):
        return self.old_collar

    def get_canyon(self):
        return self.canyon

    def get_group(self):
        return self.group

    def get_sex(self):
        return self.sex

    def get_weight(self):
        return self.weight

    def get_seconds_off(self):
        return self.seconds_off

    def get_daily_offset(self):
        return self.daily_offset

    def get_data_points(self):
        return self.data_points

    def add_comment(self, comment):
        self.comments.append(comment)

    def get_date_on(self):
        return self.date_on

    def get_date_off(self):
        return self.date_off


class BaseStation(ICollar):
    def __init__(self, collar_id):
        ICollar.__init__(self, collar_id)
        self.collar_id = collar_id
        self.encounters = []

    def get_base_station_id(self):
        return self.collar_id


class Encounter:
    def __init__(self, personal_id, record_id, enc_id, date, start_time, length):
        self.personal_id = personal_id
        self.record_id = record_id
        self.enc_id = enc_id
        current_date = date + "/2017"
        current_date = current_date.split("/")
        self.date = datetime.date(int(current_date[2]), int(current_date[1]), int(current_date[0]))
        self.start_time = start_time.split(":")
        self.full_date = self.set_full_date(current_date, self.start_time)
        self.length = int(length)

    def set_full_date(self, current_date, start_time):
        d = datetime.datetime(int(current_date[2]), int(current_date[1]), int(current_date[0]), int(start_time[0]),
                              int(start_time[1]), int(start_time[2]))
        return d

    def get_personal_id(self):
        return self.personal_id

    def get_full_date(self):
        return self.full_date

    def get_length(self):
        return self.length


class DateAndTime:
    def __init__(self, day, second, dates):
        self.day = day
        self.second = second
        self.dates = dates
        self.date = self.dates.get(self.day)

    def create_stamp(self):
        d = self.dates.get(self.day)
        t = datetime.time()

