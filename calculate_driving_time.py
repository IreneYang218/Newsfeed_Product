import datetime
import simplejson
import urllib.request

from user_definition import *

output_file = open(output_file_name, "a")
# https://developers.google.com/maps/documentation/javascript/get-api-key
apikey = 'AIzaSyBqmLunPQRrCyh55kLoktuDTC5jhq8Qjn8'
url = "https://maps.googleapis.com/maps/api/distancematrix/" +\
      "json?key=" + str(apikey) +\
      "&origins=" + str(orig_coord) + "&destinations=" + str(dest_coord) +\
      "&mode=driving&departure_time=now&language=en-EN&sensor=false"
result = simplejson.load(urllib.request.urlopen(url))
driving_time = result['rows'][0]['elements'][0]['duration_in_traffic']['text']

output_file.write(str(datetime.datetime.now()) + "\n")
output_file.write(result['origin_addresses'][0] + "\n")
output_file.write(result['destination_addresses'][0] + "\n")
output_file.write(driving_time + "\n\n")

output_file.close()
