import skyfield
from skyfield.api import load, wgs84, EarthSatellite
import io
from skyfield.iokit import parse_tle_file
import datetime as dt

def satelliteParser():
    #files and opens the file
    with open('sltrack_iridium_perm_small.txt', 'r') as file:
        #reads all lines into a list
        lines = file.readlines()  
        satelliteList = []


        #skips the first line which is the data
        #the range function allows to increment by 3 lines 
        #and start at line 1 instead of 0 and 
        #go to the end of the file
        for i in range(1, len(lines)):
            singleSatellite = []
            #takes each of the lines and gives them a 
            #corresponding variable
            temp = lines[i].split(",")
            name = temp[0].strip()
            tle1 = temp[1].strip()
            tle2 = temp[2].strip()
            NORADid = tle1[2:7]
            #loads the timescale using the 
            #official Earth Rotation data
            singleSatellite.append(name)
            singleSatellite.append(NORADid)
            singleSatellite.append(tle1)
            singleSatellite.append(tle2)

            satelliteList.append(singleSatellite)

    return satelliteList
templist = satelliteParser()


def satelliteFinderID(ID):
    for element in templist:
        if(element[1] == ID):
            return element
        

def latandlongAtTime(number,time):
    # ts = load.timescale()
    tempsatellite = satelliteFinderID(number)
    #Gets the satellite data loaded from a tle
    satellite = EarthSatellite(tempsatellite[2], tempsatellite[3], tempsatellite[0])

    #Gets the current realtime timescale
    # t = ts.from_datetime(time)
    #Gets the satellite's position
    geocentric = satellite.at(time)
    #finds the latitude and longitude of the satellite
    lat, lon = wgs84.latlon_of(geocentric)

    #prints all the data
    print('Name:', tempsatellite[0])
    print('Latitude:', lat)
    print('Longitude:', lon)

def latandlongFunction(number):
    ts = load.timescale()
    tempsatellite = satelliteFinderID(number)
    #Gets the satellite data loaded from a tle
    satellite = EarthSatellite(tempsatellite[2], tempsatellite[3], tempsatellite[0])

    #Gets the current realtime timescale
    t = ts.now()
    #Gets the satellite's position
    geocentric = satellite.at(t)
    #finds the latitude and longitude of the satellite
    lat, lon = wgs84.latlon_of(geocentric)

    #prints all the data
    print('Name:', tempsatellite[0])
    print('Latitude:', lat)
    print('Longitude:', lon)



ts = load.timescale()
t1 = ts.now()
testtime = dt.datetime.now(dt.timezone.utc) 
t = ts.from_datetime(testtime) +1
latandlongAtTime('25104',t1)

latandlongAtTime('25104',t)
latandlongFunction('25104')






# # Load the JPL ephemeris DE421 (covers 1900-2050).
# planets = load('de421.bsp')
# earth, mars = planets['earth'], planets['mars']

# # What's the position of Mars, viewed from Earth?
# astrometric = earth.at(t).observe(mars)
# ra, dec, distance = astrometric.radec()

# # print(ra)
# # print(dec)
# # print(distance)

# from skyfield.api import N, W, S, E, wgs84

# Roanoke = earth + wgs84.latlon(33.868 * S, 151.2093 * W)
# astrometric = Roanoke.at(t).observe(mars)
# alt, az, d = astrometric.apparent().altaz()

# print(alt)
# print(az)

