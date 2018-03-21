## --install libraries such as flask,pyodbc--

from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session
import os
import sys
import smtplib
import pyodbc
import random
import hashlib

##For Python 2.x version use this import statements
##from email.MIMEMultipart import MIMEMultipart
##from email.MIMEText import MIMEText

##For Python 3.x version use this import statements
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
app = Flask(__name__)

## --Root Directory of the app--
@app.route('/')
def home():
    if not session.get('loginsuccess'):
        session['hashkey']=''
        return render_template('login.html')
    else:
        return "<h3>Your are successfully logged in</h3><div style='float:right'><form action='/logout' method='post'><button type='submit'>Logout</button></form></div>"

## --function to send Email to new users-- and make sure the file is currently running in port 8081
def sendEmail(firstname,hashkey,email):
    try:
        fromaddr = "labt9000@gmail.com"
        toaddr = email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Account Activation Required"
         
        body =  """Hi {0},\n\n
Thanks for signing up!Click on the below link to get your account activate.\n


http://localhost:8081/verify?user={1}&key={2}""".format(firstname,firstname,str(hashkey))
        msg.attach(MIMEText(body, 'plain'))
         
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "demo@1234")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        return ('Success')
    except:
        return ('Error')

## --function to insert new users in sqlDB--
def insertuser(firstname,lastname,mailid,phonenumber,hashkey):
    try:
        conn = pyodbc.connect(r'Driver={SQL Server};Server=.\SQLEXPRESS;Database=RakeshDB;Trusted_Connection=yes;')
        cursor = conn.cursor()
        sql="insert into TransportApp_signin (FirstName,LastName,Email,PhoneNumber,Hashkey) values(?,?,?,?,?)"
        params=(firstname,lastname,mailid,phonenumber,hashkey)
        cursor.execute(sql,params)
        conn.commit()
        conn.close()
        return ('Success')
    except:
        return ('Error')
    
## --function to check if the user has activated the account--
def checkexisting_user(user,key):
    try:
        conn = pyodbc.connect(r'Driver={SQL Server};Server=.\SQLEXPRESS;Database=RakeshDB;Trusted_Connection=yes;')
        cursor = conn.cursor()
        sql="select FirstName,Email,Hashkey from TransportApp_signin where FirstName = ? and Hashkey = ? and active = 0"
        params=(user,key)
        cursor.execute(sql,params)
        count =0;
        for row in cursor.fetchall():
            count = count+1
        conn.close() 
        return count
    except:
        return 'Error'

## --function to set the password for the new signup--
def updatePassword(password,hashkey):
    try:
        conn = pyodbc.connect(r'Driver={SQL Server};Server=.\SQLEXPRESS;Database=RakeshDB;Trusted_Connection=yes;')
        cursor = conn.cursor()
        sql="update TransportApp_signin set Password = ? , active = 1 where Hashkey = ?"
        params=(str(password),hashkey)
        cursor.execute(sql,params)
        conn.commit()
        conn.close()
        return ('Success')
    except:
        return ('Error')

## --function to login to the site--
def loginuser(username,password):
    try:
        conn = pyodbc.connect(r'Driver={SQL Server};Server=.\SQLEXPRESS;Database=RakeshDB;Trusted_Connection=yes;')
        cursor = conn.cursor()
        sql="select * from TransportApp_signin where Email = ? and Password = ? and active = 1"
        params=(username,password)
        cursor.execute(sql,params)
        count =0;
        for row in cursor.fetchall():
            count = count+1
        conn.close()
        return count
    except:
        return ('Error')
    
## --function to get the form details of signup--
@app.route('/signup', methods=['POST'])
def signUp_user():
    firstname=request.form['firstname']
    lastname=request.form['lastname']
    mailid=request.form['email']
    phonenumber=request.form['phonenumber']
    hashkey=hashlib.md5(str(random.randint(0,1000))).hexdigest()
    result=insertuser(firstname,lastname,mailid,phonenumber,hashkey)
    if result == 'Success':
        res = sendEmail(firstname,hashkey,mailid)
        if res == 'Success':
            flash('Please check your email for account activation ')
        else:
            flash('Error Occured  !!!')
    else:
        flash('Error Occured while signup')
    return home()
    
## -- function to activate the account and redirecting to setPassword page--
@app.route('/verify',methods=['GET'])
def verifyUser():
    firstname=request.args.get('user')
    key=request.args.get('key')
    session['hashkey']=key
    result = checkexisting_user(firstname,key)
    if result == 1:
        flash("Set password for your account")
        return render_template('setPassword.html')
    else:
        flash("Please check your mail for your correct activation link !!!")
        return home()

## --getting the password using form and redirecting to login page--
@app.route('/setpassword',methods=['POST'])
def setPassword():
    password=hashlib.md5(request.form['password']).hexdigest()
    result = updatePassword(password,str(session['hashkey']))
    if result == 'Success':
        flash("Password set successfully !! Login to continue")
        return home()
    else:
        flash("Error occured while setting password")
        return home()
    
## --function to get the logindetails using form--
@app.route('/signin',methods=['POST'])
def signin_User():
    username=request.form['username']
    password=hashlib.md5(request.form['password']).hexdigest()
    result = loginuser(username,str(password))
    if result == 1:
        session['loginsuccess']=True
        return home()
    else:
        flash("Pleas Signup or check your mail for activation")
        return home()

## -- function  to logout from the application--
@app.route('/logout',methods=['POST'])
def logout():
    session['loginsuccess']=False
    return home()
    
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(port=8081)
