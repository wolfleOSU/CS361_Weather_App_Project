import socket
import requests
import geocoder
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.distance import distance



def printDetails(ip):
    res = DbIpCity.get(ip, api_key="free")
    print(f"IP Address: {res.ip_address}")
    print(f"Location: {res.city}, {res.region}, {res.country}")
    print(f"Coordinates: (Lat: {res.latitude}, Lng: {res.longitude})")

g = geocoder.ip('me')

if g.ok:
    printDetails(g.ip)
else:
    print("Failed to get user location data")
