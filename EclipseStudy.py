import skyfield
from skyfield.api import load, wgs84, EarthSatellite, N, W,utc
import io
from skyfield.iokit import parse_tle_file
# import datetime as dt
from datetime import datetime as dt
import numpy as np
from matplotlib import pyplot as plt

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
    print('Altitude:', alt.degrees)
    print('Azimuth:', az.degrees)
    # print('Distance: {:.1f} km'.format(distance.km))
    return [alt.radians, az.radians]

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
out = [0]*23
for x in range(0,23):
    # (part 2) edites the generic time with int values
    realTime = testtime.replace(year = 2024, day = 30, month = 3, minute= 50, hour = x, second= 0, microsecond=0)
    # Reason 1 why skyfield is annoying: it needs its own datatype for time calculations 
    # but that datatype can only be generated with datetime classes 
    t = ts.from_datetime(realTime)

    # gets the distance vector for a satellite
    postemp = positionAtTime('41866',t,blacksburg)
    pos1 = [np.sin(np.pi/2-postemp[0])*np.cos(postemp[1]),np.sin(np.pi/2-postemp[0])*np.sin(postemp[1]),np.cos(np.pi/2-postemp[0])]
    print(pos1)


    goeblacksburg = earth+ wgs84.latlon(37.2296 * N, 80.4139 * W)
    astrometric = goeblacksburg.at(t).observe(sun)
    alt, az, d = astrometric.apparent().altaz()
    pos2 = [np.sin(np.pi/2-alt.radians)*np.cos(az.radians),np.sin(np.pi/2-alt.radians)*np.sin(az.radians),np.cos(np.pi/2-alt.radians)]
    print(alt.degrees)
    print(az.degrees)
    print(pos2)
    out[x] = np.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2+(pos1[2]-pos2[2])**2)


print(out)
x = np.arange(23)
plt.figure()
plt.plot(x,out,'o',color = 'g')
plt.show



