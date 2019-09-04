# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 17:09:28 2019

@author: Ankita
"""
import os
from flask import Flask, request, render_template, redirect, url_for,flash
import sqlite3
import geocoding
import KNN
import DonorKNN
app= Flask(__name__)

import os.path

BASE_DIR = r"C:\Users\Ankita\Desktop"
db_path = os.path.join(BASE_DIR, "BloodGroup.db")

@app.route('/')
def form():
	return """
        <html>
            <body>
                <h1>Blood Donation</h1>

                <form action="/transform" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file" />
                    <input type="file" name="data_file2" />
                    <input type="submit" name="Submit" value="Submit" />
                </form>
                
            </body>
        </html>
    	"""

@app.route('/registerwho', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        u_reg=request.form['reg']
        error = 'Invalid Credentials. Please try again.'
        #return redirect(url_for('home'))
        if(u_reg=='user'):
            return(render_template('registeruser.html', error=error))
        else:
            return render_template('registercamp.html', error=error)
    return render_template('registerwho.html',error=error)

@app.route('/registeruser', methods=['GET', 'POST'])
def registeruser():
    #error = None
    if request.method == 'POST':
        u_fname=request.form['userfirstname']
        u_lname=request.form['userlastname']
        u_dob=request.form['dob']
        u_phonenumber=request.form['phonenumber']
        u_bloodgroup=request.form['bloodgroup']
        u_email=request.form['email']
        u_password=request.form['password']
        u_address=request.form['address']
        u_city=request.form['city']
        u_state=request.form['state']
        u_country=request.form['country']
        u_pincode=request.form['pincode']
       # error = 'Invalid Credentials. Please try again.'
      #  return redirect(url_for('home'))
        ADDRESS=u_address+" "+u_city+" "+u_state+" "+u_country
        lat,long=geocoding.GEO(ADDRESS)
        print(lat,long)
        conn=sqlite3.connect(db_path)
        cur=conn.cursor()
        #cur.execute("select * from User")
        #data=cur.fetchall()
        #for row in data:
        #    print(row[0])
        #    print(row[1])
        cur.execute("INSERT INTO User(FirstName,LastName,DOB,PhoneNumber,BloodGroup,Email,Password,Address,City,State,Country,Pincode,Latitude,Longitude) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(u_fname,u_lname,u_dob,u_phonenumber,u_bloodgroup,u_email,u_password,u_address,u_city,u_state,u_country,u_pincode,lat,long))
        conn.commit()
        ID=cur.lastrowid
        print(ID)
        #flash("thanks for registering")
    return "Your UserId is "+str(ID)+" !\n Please write it somewhere."

@app.route('/registercamp', methods=['GET', 'POST'])
def registercamp():
    #error = None
    if request.method == 'POST':
        c_name=request.form['campname']
        c_organizer=request.form['organizer']
        c_phonenumber=request.form['phonenumber']
        c_email=request.form['email']
        c_password=request.form['password']
        c_address=request.form['address']
        c_city=request.form['city']
        c_state=request.form['state']
        c_country=request.form['country']
        c_pincode=request.form['pincode']
        c_date=request.form['date']
        c_starttime=request.form['starttime']
        c_endtime=request.form['endtime']
       # error = 'Invalid Credentials. Please try again.'
      #  return redirect(url_for('home'))
        ADDRESS=c_address+" "+c_city+" "+c_state+" "+c_country
        lat,long=geocoding.GEO(ADDRESS)
        print(lat,long)
        conn=sqlite3.connect(db_path)
        cur=conn.cursor()
        #cur.execute("select * from User")
        #data=cur.fetchall()
        #for row in data:
        #    print(row[0])
        #    print(row[1])
        cur.execute("INSERT INTO Camp(Name,Organizer,PhoneNumber,Email,Password,Address,City,State,Country,Pincode,Date,StartTime,EndTime,Latitude,Longitude) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(c_name,c_organizer,c_phonenumber,c_email,c_password,c_address,c_city,c_state,c_country,c_pincode,c_date,c_starttime,c_endtime,lat,long))
        conn.commit()
        ID=cur.lastrowid
        print(ID)
        #flash("thanks for registering")
    return "Your UserId is "+str(ID)+" !\n Please write it somewhere."

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u_reg=request.form['reg']
        print("u_reg=",u_reg)
        u_name=request.form['userid']
        u_name=int(u_name)
        u_password=request.form['password']
        print("u_name=",u_name,"\n u_password=",u_password)
        
        conn=sqlite3.connect(db_path)
        cur=conn.cursor()
        if(u_reg=='user'):
            cur.execute("SELECT Id,Password from User where Id={}".format(u_name))
            data=cur.fetchall()
            for i in data:
                uid=i[0]
                upass=i[1]
                print(uid,upass)
            print(u_name == uid)
            print(u_password == upass)
            if((u_name == uid)and(u_password == upass)):
                print(u_name,"==",uid)
                return render_template("home.html")
        elif(u_reg=='camp'):
            cur.execute("SELECT Id,Password from Camp where Id={}".format(u_name))
            data=cur.fetchall()
            for i in data:
                uid=i[0]
                upass=i[1]
                print(uid,upass)
            if(u_name==uid)and(u_password==upass):
                return render_template('home.html')
        #error = 'Invalid Credentials. Please try again.'
            #return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/list.html')
def list():
    return render_template('list.html')

@app.route('/camplist', methods=['GET', 'POST'])
def camplist():
    #error = None
    if request.method == 'POST':
        u_userid=request.form['userid']
       # u_userid=int(u_userid)
        conn=sqlite3.connect(db_path)
        cur=conn.cursor()
        cur.execute("select Latitude,Longitude from User where Id="+u_userid)
        data=cur.fetchall()
        for row in data:
            lat=row[0]
            lat=float(lat)
            print(row[0])
            long=row[1]
            long=float(long)
            print(row[1])
        campid=[]    
        campid=KNN.Knn(lat,long)
        print("In app.py")
        print(campid)
        campid=tuple(campid)
        campid=str(campid)
        print("select * from Camp where Id in"+campid)
        cur.execute("select * from Camp where Id in"+campid)
        data1=cur.fetchall()
        print(data1)
        return render_template('list.html',data1=data1)
    return render_template('camplist.html')

@app.route('/registerdonor', methods=['GET', 'POST'])
def registerdonor():
    #error = None
    if request.method == 'POST':
        u_fname=request.form['userfirstname']
        u_lname=request.form['userlastname']
        u_dob=request.form['dob']
        u_phonenumber=request.form['phonenumber']
        u_bloodgroup=request.form['bloodgroup']
        u_email=request.form['email']
        u_password=request.form['password']
        u_address=request.form['address']
        u_city=request.form['city']
        u_state=request.form['state']
        u_country=request.form['country']
        u_pincode=request.form['pincode']
        u_status='1'
       # error = 'Invalid Credentials. Please try again.'
      #  return redirect(url_for('home'))
        ADDRESS=u_address+" "+u_city+" "+u_state+" "+u_country
        lat,long=geocoding.GEO(ADDRESS)
        print(lat,long)
        conn=sqlite3.connect(db_path)
        cur=conn.cursor()
        cur.execute("INSERT INTO Donor(FirstName,LastName,DOB,PhoneNumber,BloodGroup,Email,Password,Address,City,State,Country,Pincode,Latitude,Longitude,Status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(u_fname,u_lname,u_dob,u_phonenumber,u_bloodgroup,u_email,u_password,u_address,u_city,u_state,u_country,u_pincode,lat,long,u_status))
        conn.commit()
        ID=cur.lastrowid
        print(ID)
        #flash("thanks for registering")
        return "Your DonorId is "+str(ID)+" !\n Please write it somewhere."
    return render_template('registerdonor.html')

@app.route('/finddonor', methods=['GET', 'POST'])
def finddonor():
    #error = None
    if request.method == 'POST':
        u_userid=request.form['userid']
        u_bg=request.form['bloodgroup']
       # u_userid=int(u_userid)
        conn=sqlite3.connect(db_path)
        cur=conn.cursor()
        cur.execute("select Latitude,Longitude from User where Id="+u_userid)
        data=cur.fetchall()
        for row in data:
            lat=row[0]
            lat=float(lat)
            print(row[0])
            long=row[1]
            long=float(long)
            print(row[1])
        donorid=[]    
        donorid=DonorKNN.Knn(lat,long,u_bg)
        print("In app.py")
        print(donorid)
        donorid=tuple(donorid)
        donorid=str(donorid)
        print("select * from Donor where Id in"+donorid)
        cur.execute("select * from Donor where Id in"+donorid)
        data1=cur.fetchall()
        print(data1)
        return render_template('donorlist.html',data1=data1)
    return render_template('finddonor.html')

if __name__ == '__main__':
    app.run(debug=True)

