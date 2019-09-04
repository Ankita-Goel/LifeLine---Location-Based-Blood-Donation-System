# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 23:49:01 2019

@author: Ankita
"""
def GEO(address):
    
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="API KEY")
    location = geolocator.geocode(address)
    print(location.address)
    lat=location.latitude
    long=location.longitude
    print((location.latitude, location.longitude))
    return lat,long
   