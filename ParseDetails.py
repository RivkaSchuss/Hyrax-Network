# coding: utf-8
import csv
import ICollar
import sys, traceback
import datetime

hyrax_dict = {}
basestation_dict={}

real_data_path = "C:\Users\Avihay Arzuan\Desktop\לימודים\פרויקט\data\Proximity_data\proximity_loggers\Real Data"
proximity_loggers_path = "C:\Users\Avihay Arzuan\Desktop\לימודים\פרויקט\data\Proximity_data\proximity_loggers\Proximity_loggers.csv"
with open(proximity_loggers_path) as f:
    reader = csv.reader(f)
    first_row = next(reader)
    attribute_list = first_row[0].split(";")
    attribute_list[0] = "collar_id"
    print attribute_list

    i = 1
    while True:
        try:
            row = next(reader)
            line = row[0]
            split_line = line.split(';')
            if split_line[attribute_list.index("Tag")] == "Basestation":
                basestation_dict[split_line[0]] = ICollar.BaseStation(split_line[0])
                continue
            if split_line[attribute_list.index("Date_on")] == "":
                continue
            if split_line[attribute_list.index("Date_off")] == "":
                continue
            if split_line[attribute_list.index("Tag")] == "AK":
                continue
            hyrax_dict[int(split_line[0])] = ICollar.Hyrax(split_line[0],split_line, real_data_path)
        except Exception:
            #traceback.print_exc(file=sys.stdout)
            break
        i+=1
        f.close

#for key, hyrax in hyrax_dict.iteritems():
#    hyrax.print_details()

#for key, station in basestation_dict.iteritems():
#    print station.get_base_station_id()
   
date_on_dict = {}
date_off_dict = {}
last_on = datetime.date(2000, 1,1)
first_off = datetime.date(2030, 1,1)
for key, hyrax in hyrax_dict.iteritems():
    date_on_str = hyrax.get_date_on()[0].split("/")
    d_on = int(date_on_str[0])
    m_on = int(date_on_str[1])
    y_on = int(date_on_str[2])

    date_off_str = hyrax.get_date_off()[0].split("/")
    d_off = int(date_off_str[0])
    m_off = int(date_off_str[1])
    y_off = int(date_off_str[2])
    if last_on < datetime.date(y_on, m_on, d_on):
        last_on = datetime.date(y_on, m_on, d_on)

    if first_off > datetime.date(y_off,m_off,d_off):
        first_off = datetime.date(y_off, m_off, d_off)
#print last_on
#print first_off

#for key, hyrax in hyrax_dict.iteritems():
    #tag = hyrax.get_tag()
    #number = hyrax.get_hyrax_id()
    #data_path = real_data_path + "\\logger"+ number + "_" + tag + ".csv"
    #print hyrax.get_real_data_path()

#hyrax = hyrax_dict.get(2)

for key,hyrax in hyrax_dict.iteritems():
    
    hyrax = hyrax_dict.get(key)
    with open(hyrax.get_real_data_path()) as f:
        reader = csv.reader(f)
        first_row = next(reader)
        while True:
            try:
                row = next(reader)
                meeting = ICollar.Encounter(row[0],row[1],row[2],row[3],row[4])
                hyrax.add_encounter(row[0],meeting)
                #print row
            except Exception:
                break
        f.close
    
print first_row

print "ss"
