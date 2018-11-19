import datetime
from astral import Astral

print "testtttt"
print "test 2"
print "shalommmmm"

a = Astral()
a.solar_depression = 'civil'
city_name = 'Jerusalem'
city = a[city_name]

print('Information for %s/%s\n' % (city_name, city.country))

timezone = city.timezone
print('Timezone: %s' % timezone)

print('Latitude: %.02f; Longitude: %.02f\n' % (city.latitude, city.longitude))

sun = city.sun(date=datetime.date(2017, 6, 22), local=True)
print('Dawn:    %s' % str(sun['dawn']))
print('Sunrise: %s' % str(sun['sunrise']))
print('Noon:    %s' % str(sun['noon']))
print('Sunset:  %s' % str(sun['sunset']))
print('Dusk:    %s' % str(sun['dusk']))
