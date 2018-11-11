class ICollar:

    def __init__(self, collar_id):
        self.collar_id = collar_id
        self.encounters = []
        self.filtered_encounters = []

    def add_encounter(self, enc_id, encounter):
        self.encounters[enc_id] = encounter


class Hyrax(ICollar):
    def __init__(self, collar_id, serial_number, chip, tag, old_collar, canyon, group, sex, weight, date_on, date_off,
                 seconds_off, daily_offset, data_points, comments):
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

    def get_hyrax_id(self):
        return self.collar_id

    def add_comment(self, comment):
        self.comments.append(comment)


class BaseStation(ICollar):
    def __init__(self, collar_id):
        ICollar.__init__(self, collar_id)
        self.collar_id = collar_id
        self.encounters = []

    def get_base_station_id(self):
        return self.collar_id


class Encounter:
    def __init__(self, record_id, enc_id, date, start_time, length):
        self.record_id = record_id
        self.enc_id = enc_id
        self.date = date.split("/")
        self.start_time = start_time.split(":")
        self.length = length
