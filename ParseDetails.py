# coding: utf-8
import csv
import ICollar
import sys, traceback

hyrax_dict = {}

with open("C:\Users\Avihay Arzuan\Desktop\לימודים\פרויקט\data\Proximity_data\proximity_loggers\Proximity_loggers.csv") as f:
    reader = csv.reader(f)
    first_row = next(reader)
    #print first_row
    attribute_list = first_row[0].split(";")
    attribute_list[0] = "collar_id"
    print attribute_list

    i = 1
    while True:
        try:
            row = next(reader)
            #number = row[0]
            line = row[0]
            splitted = line.split(';')
            hyrax_dict[splitted[0]] = ICollar.Hyrax(splitted[0],splitted)
            #hyrax_dict[number] = ICollar.Hyrax(splitted[0],splitted[1],splitted[2],splitted[3],splitted[4]
            #                                   ,splitted[5],splitted[6],splitted[7],splitted[8],splitted[9]
            #                               ,splitted[10],splitted[11],splitted[12],splitted[13],splitted[14])
        except Exception:
            #traceback.print_exc(file=sys.stdout)
            break
        i+=1

for key, hyrax in hyrax_dict.iteritems():
    hyrax.print_details()

#for key, hyrax in hyrax_dict.iteritems():
