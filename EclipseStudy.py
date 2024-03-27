import skyfield
from skyfield.api import load, wgs84, EarthSatellite, N, W,utc
import io
from skyfield.iokit import parse_tle_file
# import datetime as dt
from datetime import datetime as dt
import numpy as np

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
        

def positionAtTime(number,time,position):
    tempsatellite = satelliteFinderID(number)
    #Gets the satellite data loaded from a tle
    satellite = EarthSatellite(tempsatellite[2], tempsatellite[3], tempsatellite[0])

    difference = satellite - position
    #Gets the satellite's position
    satFromDiff = difference.at(time)

    alt, az, distance = satFromDiff.altaz()
    print('Altitude:', alt)
    print('Azimuth:', az)
    print('Distance: {:.1f} km'.format(distance.km))
    return [satFromDiff.position.au[0],satFromDiff.position.au[1],satFromDiff.position.au[2]]

def latandlongFunction(number):
    #Gets the current realtime timescale
    ts = load.timescale()
    t = ts.now()
    tempsatellite = satelliteFinderID(number)

    #Gets the satellite data loaded from a tle
    satellite = EarthSatellite(tempsatellite[2], tempsatellite[3], tempsatellite[0])

    #Gets the satellite's position
    geocentric = satellite.at(t)

    return [geocentric.position.au[0],geocentric.position.au[1],geocentric.position.au[2]]


ts = load.timescale()
planets = load('de421.bsp')  # ephemeris DE421
sun = planets['sun']
earth = planets['Earth']
blacksburg = wgs84.latlon(37.2296 * N, 80.4139 * W)

# use this to get time       
# best way I could find to generate a general time (part 1)
# makes a generic time to be changed later
testtime = dt.fromisoformat('2011-11-04 00:05:23.283')
testtime= testtime.replace(tzinfo=utc)      # to fix an existing datetime

# (part 2) edites the generic time with int values
realTime = testtime.replace(year = 2024, day = 27, month = 3, minute= 0, hour = 9, second= 0, microsecond=0)
# Reason 1 why skyfield is annoying: it needs its own datatype for time calculations 
# but that datatype can only be generated with datetime classes 
t = ts.from_datetime(realTime)

# gets the distance vector for a satellite
pos1 = positionAtTime('25104',t,blacksburg)

# I believe this gives altidute and azimuth in radians but I'm working on verifying
# also don't know where origin is
azpos1 = np.arccos(pos1[2]/(np.sqrt(pos1[0]**2+pos1[1]**2+pos1[2]**2)))
altpos1 = np.arctan(-pos1[1]/pos1[0])

print(azpos1*(180/np.pi))
print(altpos1*(180/np.pi))

goeblacksburg = earth+ wgs84.latlon(37.2296 * N, 80.4139 * W)
astrometric = goeblacksburg.at(t).observe(sun)
alt, az, d = astrometric.apparent().altaz()
print(alt)
print(az)


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

