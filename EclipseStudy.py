import skyfield
from skyfield.api import load, wgs84
import io
from skyfield.iokit import parse_tle_file

x = open("sltrack_iridium_perm_small.txt", "r")

TLEstring = x.read()
S = TLEstring.strip().split(',')
print(TLEstring)
print(S)








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

