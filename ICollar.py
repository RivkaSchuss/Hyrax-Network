class ICollar:

    def __init__(self, collar_id):
        self.collar_id = collar_id
        self.encounters = []
        self.filtered_encounters = []

    def add_encounter(self, enc_id, encounter):
        self.encounters[enc_id] = encounter


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

    def set_value(self, array,i):
        try:
            value = array[i]
        except IndexError:
            value = ""
        return value

    def __init__(self, collar_id, array):
        ICollar.__init__(self,collar_id)
        i=0
        self.collar_id = self.set_value(array,i)
        i+=1
        self.serial_number = self.set_value(array,i)
        i+=1
        self.chip = self.set_value(array,i)
        i+=1
        self.tag = self.set_value(array,i)
        i+=1
        self.old_collar = self.set_value(array,i)
        i+=1
        self.canyon = self.set_value(array,i)
        i+=1
        self.group = self.set_value(array,i)
        i+=1
        self.sex = self.set_value(array,i)
        i+=1
        self.weight = self.set_value(array,i)
        i+=1
        self.date_on = self.set_value(array,i)
        i+=1
        self.date_off = self.set_value(array,i)
        i+=1
        self.seconds_off = self.set_value(array,i)
        i+=1
        self.daily_offset = self.set_value(array,i)
        i+=1
        self.data_points = self.set_value(array,i)
        i+=1
        self.comments = self.set_value(array,i)
        i+=1

    def get_hyrax_id(self):
        return self.collar_id

    def add_comment(self, comment):
        self.comments.append(comment)

    def print_details(self):
        print "collar_id" + self.collar_id
        print self.serial_number 
        print self.chip
        print self.tag
        print self.old_collar
        print self.canyon
        print self.group
        print self.sex
        print self.weight
        print "date on:" + self.date_on
        print "date off:" + self.date_off
        print self.seconds_off
        print self.daily_offset
        print self.data_points
        print self.comments


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
