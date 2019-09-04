# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 20:23:51 2019

@author: Ankita
"""
import sqlite3
import os.path
import math

BASE_DIR = r"C:\Users\Ankita\Desktop"
db_path = os.path.join(BASE_DIR, "BloodGroup.db")

def Knn(Lati,Longi,bg):
    Coord=[]
    con=sqlite3.connect(db_path)
    cur=con.cursor()
    print("select Id,Latitude,Longitude from Donor where BloodGroup=""'"+bg+"'")
    cur.execute("select Id,Latitude,Longitude from Donor where BloodGroup=""'"+bg+"'")
    data=cur.fetchall()
    for row in data:
        Point=[]
        donor_id=row[0]
        donor_id=int(donor_id)
        Point.append(donor_id)
        lat=row[1]
        lat=float(lat)
        print(row[1])
        Point.append(lat)
        long=row[2]
        long=float(long)
        Point.append(long)
        print(row[2])
        Coord.append(Point)
    print(Coord)
    #calculate the euclidean distance of p from training points 
    distance=[]
    for i in Coord:
        dis=[]
        #print(i)
        #print(i[1],i[2])
        euclidean_distance = math.sqrt((i[1]-Lati)**2 +(i[2]-Longi)**2)
        dis.append(i[0])
        dis.append(euclidean_distance)
        distance.append(dis)
        #print(distance)
     
    distance.sort(key = lambda x: x[1]) 
    print(distance)
    finallist=[]
    count=0
    for i in range(0,2):
        finallist.append(distance[count][0])
        count=count+1
    print(finallist)
    return finallist
