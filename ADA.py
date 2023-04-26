import smtplib
import base64
import time
from email.mime.text import MIMEText

from flask import Flask, request, redirect, render_template, session, jsonify, url_for
import datetime
from DBConnection import Db
app = Flask(__name__)
app.secret_key="abc"

# @app.route('/')
# def first():
#     return render_template('first.html')



@app.route('/',methods=['get','post'])
def adminlog():
    if request.method=="POST":
        username=request.form['textfield']
        password=request.form['textfield2']
        db=Db()
        res=db.selectOne("select * from login where username='"+username+"'and password='"+password+"'")
        if res is not None :
            if res['user_type']=='admin':
                session['log']='lin'
                return redirect('/admin_home')
            if res['user_type']=='hospital':
                session['lid']=res['login_id']
                session['log'] = 'lin'
                return redirect('/hospital_home')
            if res['user_type']=='doctor':
                session['lid']=res['login_id']
                session['log'] = 'lin'
                return redirect('/doctor_home')
            if res['user_type']=='lab':
                session['lid'] = res['login_id']
                session['log'] = 'lin'
                return redirect('/lab_home')
            else:
                return'invalid'
        else:
            return'invalid'
    else:
        return render_template('first.html')


@app.route('/logout')
def logout():
    session.clear()
    session['log']=""
    return redirect('/')

@app.route('/admin_home')
def adminhome():
    if session['log']=='lin':
        return render_template('admin/adminindex.html')
    else:
        return redirect('/')

@app.route('/view_doctor')
def view_doctor():
    if session['log'] == 'lin':
        db=Db()
        qry1=db.select("select * from doctor,login where login.login_id=doctor.doctor_id and login.user_type='pending'")
        print(qry1)
        return render_template('admin/DOCTOR APPROVAL.html',data=qry1)
    else:
        return redirect('/')

@app.route('/view_hospital')
def view_hospital():
    if session['log'] == 'lin':
        db=Db()
        qry=db.select("select * from hospital,login where login.login_id=hospital.hospital_id and login.user_type='pending'")
        print(qry)
        return render_template("admin/HOSPITAL APPROVAL.html" ,data=qry)
    else:
        return redirect('/')

@app.route('/view_lab')
def view_lab():
    if session['log'] == 'lin':
        db=Db()
        qry2=db.select("select * from lab,login where login.login_id=lab.lab_id and login.user_type='pending'")
        print(qry2)
        return render_template('admin/LAB APPROVAL.html',data=qry2)
    else:
        return redirect('/')

@app.route('/approveddoc')
def approveddoc():
    if session['log'] == 'lin':
        db=Db()
        doc=db.select("select * from doctor,login where doctor.doctor_id=login.login_id and login.user_type='doctor'")
        print(doc)
        return render_template('admin/APPROVED DOCTORS.html',data=doc)
    else:
        return redirect('/')

@app.route('/approvedhos')
def approvedhos():
    if session['log'] == 'lin':
        db=Db()
        hos=db.select("select * from hospital,login where hospital.hospital_id=login.login_id and login.user_type='hospital'")
        print(hos)
        return render_template('admin/APPROVED HOSPITALS.html',data=hos)
    else:
        return redirect('/')

@app.route('/approvedlab')
def approvedlab():
    if session['log'] == 'lin':
        db=Db()
        lab1=db.select("select * from lab,login where lab.lab_id=login.login_id and login.user_type='lab'")
        print(lab1)
        return render_template('admin/APPROVED LABS.html',data=lab1)
    else:
        return redirect('/')

@app.route('/approvedclient')
def approvedclient():
    if session['log'] == 'lin':
        db=Db()
        client1 = db.select("select * from client")
        print(client1)
        return render_template('admin/VIEW CLIENTS.html' , data=client1)
    else:
        return redirect('/')

@app.route('/approve_hospital/<h_id>')
def approve_hospital(h_id):
    if session['log'] == 'lin':
        db=Db()
        db.update("update login set user_type='hospital' where login_id='"+str(h_id)+"'")
        return '<script> alert("approved"); window.location="/view_hospital"</script>'
    else:
        return redirect('/')

@app.route('/reject_hospital/<h_id>')
def reject_hospital(h_id):
    if session['log'] == 'lin':
        db=Db()
        db.delete("delete from hospital where hospital_id='"+str(h_id)+"'")
        db.delete("delete from login where login_id='"+str(h_id)+"'")
        return '<script> alert("rejected"); window.location="/view_hospital"</script>'
    else:
        return redirect('/')

@app.route('/approve_doctor/<d_id>')
def approve_doctor(d_id):
    if session['log'] == 'lin':
        db=Db()
        db.update("update login set user_type='doctor' where login_id='"+str(d_id)+"'")
        return '<script> alert("approved"); window.location="/view_doctor"</script>'
    else:
        return redirect('/')

@app.route('/reject_doctor/<d_id>')
def reject_doctor(d_id):
    if session['log'] == 'lin':
        db=Db()
        db.delete("delete from doctor where doctor_id='" + str(d_id) + "'")
        db.delete("delete from login where login_id='" + str(d_id) + "'")
        return '<script> alert("rejected"); window.location="/view_doctor"</script>'
    else:
        return redirect('/')

@app.route('/approve_lab/<l_id>')
def approve_lab(l_id):
    if session['log'] == 'lin':
        db=Db()
        db.update("update login set user_type='lab' where login_id='"+str(l_id)+"'")
        return '<script> alert("approved"); window.location="/view_lab"</script>'
    else:
        return redirect('/')

@app.route('/reject_lab/<l_id>')
def reject_lab(l_id):
    if session['log'] == 'lin':
        db=Db()
        db.delete("delete from lab where lab_id='" + str(l_id) + "'")
        db.delete("delete from login where login_id='" + str(l_id) + "'")
        return '<script> alert("rejected"); window.location="/view_lab"</script>'
    else:
        return redirect('/')




@app.route('/add_medicine',methods=['get','post'])
def add_medicine():
    if session['log'] == 'lin':
        if request.method=="POST":
            name=request.form['textfield']
            image=request.files['fileField']
            date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            image.save(r"C:\Users\HP\PycharmProjects\ADA\static\pic\\"+date+'.jpg')
            img="/static/pic/"+date+'.jpg'
            price=request.form['textfield2']
            details = request.form['textarea']
            db=Db()
            db.insert("insert into medicine values('','"+str(img)+"','"+name+"','"+details+"','"+price+"')")
            return '<script> alert("added succesfully"); window.location="/add_medicine"</script>'
        else:
            return render_template('admin/MEDICINE MANAGEMENT.html')
    else:
        return redirect('/')



@app.route('/view_medicine')
def view_medicine():
    if session['log'] == 'lin':
        db = Db()
        med = db.select("select * from medicine")
        print(med)
        return render_template('admin/medicine.html', data=med)
    else:
        return redirect('/')

@app.route('/test_management',methods=['get','post'])
def test_management():
    if session['log'] == 'lin':
        if request.method=="POST":
           name=request.form['textfield1']
           db = Db()
           db.insert("insert into test values('','"+name+"')")
           return '<script> alert("added succesfull"); window.location="/admin_home"</script>'
        else:
           return render_template('admin/TEST MANAGEMENT.html')
    else:
        return redirect('/')


@app.route('/view_tests')
def view_tests():
    if session['log'] == 'lin':
        db = Db()
        tes = db.select("select * from test")
        print(tes)
        return render_template('admin/VIEW TEST.html', data=tes)
    else:
        return redirect('/')

@app.route('/delete_test/<tes>')
def delete_test(tes):
    if session['log'] == 'lin':
        db = Db()
        db.delete("delete from test WHERE test_id='"+tes+"'")
        return '<script> alert("deleted succesfull"); window.location="/view_tests"</script>'
    else:
        return redirect('/')

# ======================================================================================================

#hospital area below

# ======================================================================================================
@app.route('/hospital_home')
def hospitalhome():
    db=Db()
    return render_template('hospital/hospitalindex.html')



@app.route('/hospital_registration',methods=['get','post'])
def hospital_registration():
    if request.method=="POST":
        name=request.form['textfield']
        password=request.form['textfield10']
        License_id=request.form['textfield3']
        Type=request.form['textfield4']
        Zipcode=request.form['textfield5']
        image = request.files['fileField']
        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        image.save(r"C:\Users\HP\PycharmProjects\ADA\static\pic\\" + date + '.jpg')
        img = "/static/pic/" + date + '.jpg'
        Email_id=request.form['textfield6']
        Phone_number=request.form['textfield7']
        Bio=request.form['textarea']
        latitude=request.form['textfield9']
        longitude=request.form['textfield11']
        db = Db()
        q=db.insert("insert into login values('','"+Email_id+"','"+password+"','pending')")
        db.insert("insert into hospital values('"+str(q)+"','"+name+"','"+License_id+"','"+Type+"','"+Zipcode+"','"+str(img)+"','"+Email_id+"','"+Phone_number+"','"+Bio+"','"+latitude+"','"+longitude+"')")
        return '<script> alert("registration succesfull"); window.location="/"</script>'
    else:
        return render_template('hospital/HOSPITAL REGISTRATION.html')



@app.route('/hospital_profile_management',methods=['get','post'])
def hospital_profile_management():
    if request.method=="POST":
        name=request.form['textfield']
        License_id=request.form['textfield3']
        Htype=request.form['textfield4']
        Zipcode=request.form['textfield5']
        image = request.files['fileField']
        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        image.save(r"C:\Users\HP\PycharmProjects\ADA\static\pic\\" + date + '.jpg')
        img = "/static/pic/" + date + '.jpg'
        Email_id=request.form['textfield6']
        Phone_number=request.form['textfield7']
        Bio=request.form['textarea']
        latitude=request.form['textfield9']
        longitude=request.form['textfield11']
        db = Db()
        if request.files!="":
            if image.filename!="":
                db.update("update hospital set hospital_name='"+name+"',license_id='"+License_id+"',`type`='"+Htype+"',zipcode='"+Zipcode+"',img='"+str(img)+"',email_id='"+Email_id+"',phone_number='"+Phone_number+"',bio='"+Bio+"',latitude='"+latitude+"',longitude='"+longitude+"' WHERE hospital_id='"+str(session['lid'])+"'")
                return '<script> alert("updated succesfull"); window.location="/hospital_home"</script>'
            else:
                db.update("update hospital set hospital_name='" + name + "',license_id='" + License_id + "',`type`='" + Htype + "',zipcode='" + Zipcode + "',email_id='" + Email_id + "',phone_number='" + Phone_number + "',bio='" + Bio + "',latitude='"+latitude+"',longitude='"+longitude+"' WHERE hospital_id='"+str(session['lid'])+"'")
                return '<script> alert("updated succesfull"); window.location="/hospital_home"</script>'
        else:
            db.update("update hospital set hospital_name='" + name + "',,license_id='" + License_id + "',`type`='" + Htype + "',zipcode='" + Zipcode + "',email_id='" + Email_id + "',phone_number='" + Phone_number + "',bio='" + Bio + "',latitude='"+latitude+"',longitude='"+longitude+"' WHERE hospital_id='"+str(session['lid'])+"'")
            return '<script> alert("updated succesfull"); window.location="/hospital_home"</script>'
    else:
        db=Db()
        res=db.selectOne("select * from hospital WHERE hospital_id='"+str(session['lid'])+"'")
        return render_template('hospital/HOSPITAL PROFILE MANAGEMENT.html',data=res)

#doctor contents here


@app.route('/doctor_home')
def doctorhome():
    db=Db()
    return render_template('doctor/doctorindex.html')

@app.route('/doctor_registration',methods=['get','post'])
def doctor_registration():
    if request.method=="POST":
        name =request.form['textfield1']
        password =request.form['password']
        license_id =request.form['textfield2']
        specialization =request.form['textfield3']
        bio =request.form['textarea']
        email_id =request.form['textfield4']
        phone_number =request.form['textfield5']
        gender =request.form['radio']
        schedule =request.form['textfield7']
        latitude=request.form['textfield9']
        longitude=request.form['textfield11']
        db = Db()
        qry=db.selectOne("select * from login where username='"+email_id+"'")
        if qry is not None:
            return '<script> alert("Email Already exist"); window.location="/"</script>'

        q =db.insert("insert into login values('','"+email_id+"','"+password+"','pending')")
        db.insert("insert into doctor values('"+str(q)+"','"+name+"','"+license_id+"','"+specialization+"','"+bio+"','"+email_id+"','"+phone_number+"','"+gender+"','"+schedule+"',latitude='"+latitude+"',longitude='"+longitude+"')")
        return '<script> alert("registration succesfull"); window.location="/"</script>'
    else:
        return render_template('doctor/DOCTOR REGISTRATION.html')


@app.route('/doctor_profile_management',methods=['get','post'])
def doctor_profile_management():
    if request.method=="POST":
        name =request.form['textfield1']
        license_id =request.form['textfield2']
        specialization =request.form['textfield3']
        bio =request.form['textarea']
        email_id =request.form['textfield4']
        phone_number =request.form['textfield5']
        gender =request.form['radio']
        schedule =request.form['textfield7']
        latitude=request.form['textfield9']
        longitude=request.form['textfield11']
        db = Db()
        db.update("update doctor set doctor_name='" + name + "',license_id='"+license_id+"',specialization='"+specialization+"',bio='"+bio+"',email_id='"+email_id+"',phone_number='"+phone_number+"',gender='"+gender+"',schedule='"+schedule+"',latitude='"+latitude+"',longitude='"+longitude+"' WHERE doctor_id='"+str(session['lid'])+"'")
        return '<script> alert("updated succesfull"); window.location="/doctor_home"</script>'
    else:
        db = Db()
        res=db.selectOne("select * from doctor WHERE doctor_id='" + str(session['lid'])+"'")
        return render_template('doctor/DOCTOR PROFILE MANAGEMENT.html', data=res)

@app.route('/approved_booking')
def approved_booking():
    db=Db()
    book=db.select("select * from booking,client,schedule where client.client_id=booking.client_id and schedule.schedule_id=booking.schedule_id and schedule.doctor_id='"+str(session['lid'])+"' and booking.status!='pending'")
    print(book)
    return render_template('doctor/APPROVED BOOKING.html', data=book)

@app.route('/today_booking')
def today_booking():
    db=Db()
    book=db.select("select * from booking,client,schedule where client.client_id=booking.client_id and schedule.schedule_id=booking.schedule_id and schedule.doctor_id='"+str(session['lid'])+"' and schedule.date=curdate() and booking.status='booked'")
    print(book)
    return render_template('doctor/TODAY BOOKING.html', data=book)

@app.route('/view_record/<bid>')
def view_record(bid):
    db=Db()
    record=db.select("select * from share,client_data_record where share.record_id=client_data_record.record_id and share.booking_id='"+bid+"'")
    print(record)
    return render_template('doctor/SHARED RECORD.html',data=record)

@app.route('/view_bookings')
def view_bookings():
    db=Db()
    book=db.select("select * from booking,client,schedule where booking.client_id=client.client_id and booking.schedule_id=schedule.schedule_id and schedule.doctor_id='"+str(session['lid'])+"' and status='pending'")
    print(book)
    return render_template('doctor/BOOKING APPROVAL.html', data=book)


@app.route('/approve_booking/<b_id>')
def approve_booking(b_id):
    db=Db()
    res=db.update("update booking set status='booked' where booking_id='"+b_id+"'")
    print(res)
    return '<script> alert("approved"); window.location="/approved_booking"</script>'
@app.route('/reject_booking/<b_id>')
def reject_booking(b_id):
    db=Db()
    db.delete("delete from booking where booking_id='" +b_id+ "'")
    return '<script> alert("rejected"); window.location="/approved_booking"</script>'

@app.route('/cancel_booking/<b_id>')
def cancel_booking(b_id):
    db=Db()
    db.delete("delete from booking where booking_id='" +b_id+ "'")
    return '<script> alert("cancelled"); window.location="/approved_booking"</script>'



#prescription

@app.route('/add_prescription/<bid>',methods=['get','post'])
def add_prescription(bid):
    if request.method=="POST":
        name=request.form['select']
        details=request.form['textarea']
        r=request.form['radio']
        db = Db()

        db.insert("insert into prescription VALUES ('','" + details + "','" + bid + "','" + name + "')")
        if r=="yes":
            return redirect('/iftestyes/'+bid)


        if r== "no":
            db=Db()
            db.update("update booking set status='completed' where booking_id='"+bid+"' ")
            return '<script> alert("added sucessfully"); window.location="/approved_booking"</script>'
    else:
        db=Db()
        q=db.select("select * from medicine")
        return render_template("doctor/PRESCRIPTION.html",data=q)

@app.route('/view_prescription/<b_id>')
def view_prescription(b_id):
     db = Db()
     a = db.select("select * from medicine,booking,prescription where  booking.booking_id=prescription.booking_id and medicine.medicine_id=prescription.medicine_id")
     print(a)
     return render_template('doctor/PRESCRIPTION.html', data=a)

@app.route('/iftestyes/<bid>',methods=['get','post'])
def iftestyes(bid):
    if request.method=="POST":
        bb=request.form.getlist('checkbox')
        for i in bb:
            db=Db()
            db.insert("insert into lab_test values('','"+bid+"','"+i+"')")
        return '<script> alert("added sucessfully"); window.location="/approved_booking"</script>'

    else:
        db=Db()
        a=db.select("select * from test")
        return render_template('doctor/YESPAGE.html',data=a)


#schedule
@app.route('/add_schedule',methods=['get','post'])
def add_schedule():
    if request.method == "POST":
        date=request.form['textfield']
        ftime=request.form['textfield2']
        ttime=request.form['textfield3']
        db = Db()
        qry=db.selectOne("select * from schedule where date='"+date+"' and from_time='"+ftime+"' and to_time='"+ttime+"' ")
        if qry is not None:
            return '<script> alert("Already added"); window.location="/view_schedule"</script>'

        db.insert("insert into schedule VALUES ('','"+str(session['lid'])+"','"+date+"','"+ftime+"','"+ttime+"')")
        return '<script> alert("added sucessfully"); window.location="/view_schedule"</script>'
    else:
        return render_template('doctor/ADD SCHEDULE.html')

@app.route('/view_schedule')
def view_schedule():
    db = Db()
    sch = db.select("select * from schedule WHERE doctor_id='"+str(session['lid'])+"'")
    print(sch)
    return render_template('doctor/VIEW SCHEDULE.html', data=sch)

@app.route('/delete_schedule/<de>')
def delete_schedule(de):
    db = Db()
    db.delete("delete from schedule where schedule_id='"+de+"'")
    return '<script> alert("deleted sucessfully"); window.location="/view_schedule"</script>'

@app.route('/update_schedule/<up>',methods=['get','post'])
def update_schedule(up):
    if request.method == "POST":
        date=request.form['textfield']
        ftime=request.form['textfield2']
        ttime=request.form['textfield3']
        db = Db()
        db.update("update schedule set date='"+date+"',from_time='"+ftime+"',to_time='"+ttime+"' where schedule_id='"+up+"'")
        return '<script> alert("updated sucessfully"); window.location="/add_schedule"</script>'
    else:
        db=Db()
        a=db.selectOne("select * from schedule where schedule_id='"+up+"'")
        return render_template('doctor/UPDATE SCHEDULE.html', data=a)

#user data record
@app.route('/view_user_data',methods=['get','post'])
def view_user_data():
    return render_template('doctor/doctorindex.html')


#@app.route('/send_userdata',methods=['get','post'])
#def send_userdata()

# lab
@app.route('/lab_home')
def lab_home():
    db=Db()
    return render_template('lab/labindex.html')

@app.route('/lab_registration',methods=['get','post'])
def lab_registration():
    if request.method=="POST":
        name =request.form['textfield']
        password =request.form['textfield10']
        license_id =request.form['textfield2']
        location=request.form['textfield20']
        zipcode = request.form['textfield4']
        email_id =request.form['textfield5']
        phone_number =request.form['textfield6']
        schedule =request.form['textfield7']
        latitude =request.form['textfield9']
        longitude=request.form['textfield11']
        db = Db()
        qry = db.selectOne("select * from login where username='" + email_id + "'")
        if qry is not None:
            return '<script> alert("Email Already exist"); window.location="/"</script>'


        q =db.insert("insert into login values('','"+email_id+"','"+password+"','pending')")
        db.insert("insert into lab values('"+str(q)+"','"+name+"','"+license_id+"','"+location+"','"+zipcode+"','"+email_id+"','"+phone_number+"','"+schedule+"','"+latitude+"','"+longitude+"')")
        return '<script> alert("registration succesfull"); window.location="/"</script>'
    else:
        return render_template('lab/lab registration.html')


@app.route('/lab_profile_management',methods=['get','post'])
def lab_profile_management():
    if request.method=="POST":
        name =request.form['textfield']
        license_id =request.form['textfield2']
        location = request.form['textfield20']
        zipcode =request.form['textfield4']
        email_id =request.form['textfield5']
        phone_number =request.form['textfield6']
        schedule =request.form['textfield7']
        latitude =request.form['textfield9']
        longitude =request.form['textfield11']
        db = Db()
        db.update("update lab set lab_name='" + name + "',license_id='"+license_id+"',location='"+location+"',zipcode='"+zipcode+"',email_id='"+email_id+"',phone_number='"+phone_number+"',schedule='"+schedule+"',schedule='"+schedule+"',latitude='"+latitude+"',longitude='"+longitude+"' WHERE lab_id='"+str(session['lid'])+"'")
        return '<script> alert("updated succesfull"); window.location="/lab_home"</script>'
    else:
        db = Db()
        res=db.selectOne("select * from lab WHERE lab_id='" + str(session['lid'])+"'")
        return render_template('lab/lab_profile_management.html', data=res)

@app.route('/upload_test_result',methods=['get','post'])
def upload_test_result():
    if request.method=="POST":
        email=request.form['textfield']
        result=request.files['fileField']
        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        result.save(r"C:\Users\HP\PycharmProjects\ADA\static\pic\\" + date + '.pdf')
        img = "/static/pic/" + date + '.pdf'
        db=Db()
        qry=db.selectOne("select * from client where email_id='"+email+"'")
        if qry is not None:
            cid=qry['client_id']
            db.insert("insert into lab_result VALUES ('','"+str(cid)+"',curdate(),'"+str(img)+"','"+str(session['lid'])+"')")
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)

                gmail.ehlo()

                gmail.starttls()

                gmail.login('xinfomac@gmail.com', 'axauvveylehltktd')

            except Exception as e:
                print("Couldn't setup email!!" + str(e))

            msg = MIMEText("Your lab test result " + str(img))

            msg['Subject'] = 'Verification'

            msg['To'] = email

            msg['From'] = 'xinfomac@gmail.com'

            try:

                gmail.send_message(msg)

            except Exception as e:

                print("COULDN'T SEND EMAIL", str(e))
            return '''<script> alert("updated succesfull"); window.location="/view_result"</script>'''
        else:
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)

                gmail.ehlo()

                gmail.starttls()

                gmail.login('xinfomac@gmail.com', 'axauvveylehltktd')

            except Exception as e:
                print("Couldn't setup email!!" + str(e))

            msg = MIMEText("Your lab test result " + str(img))

            msg['Subject'] = 'Verification'

            msg['To'] = email

            msg['From'] = 'xinfomac@gmail.com'

            try:

                gmail.send_message(msg)

            except Exception as e:

                print("COULDN'T SEND EMAIL", str(e))
            return '''<script> alert("updated succesfull"); window.location="/view_result"</script>'''
    else:
        return render_template('lab/update result.html')

@app.route('/view_result')
def view_result():
    db=Db()
    res=db.select("select * from lab_result,client where lab_result.client_id=client.client_id and lab_result.lab_id='"+str(session['lid'])+"'")
    return render_template('lab/test_result.html', data=res)


# =============================================================================================================
#                                         client module
# ==============================================================================================================

@app.route('/and_login',methods=['post'])
def and_login():
    username = request.form['u']
    password = request.form['p']
    db = Db()
    res = db.selectOne("select * from login where username='" + username + "'and password='" + password + "'")
    if res is not None:
        return jsonify(status="ok",type=res['user_type'],lid=res['login_id'])
    else:
        return  jsonify(status="no")



@app.route('/and_view_profile', methods=['post'])
def and_view_profile():
    lid = request.form['id']
    db = Db()
    res = db.selectOne("select * from client WHERE client_id='" + str(lid)+"'")
    # print(res)
    # if len(res) > 0:
    return jsonify(status="ok", data=res)
    # else:
    #     return jsonify(status="no")

@app.route('/and_update_profile', methods=['post'])
def and_update_profile():
    lid = request.form['id']
    name=request.form['name']
    phone=request.form['phone']
    gender=request.form['gender']
    location=request.form['location']
    zipcode=request.form['zip_code']
    emergency=request.form['emergency']
    email=request.form['email']
    age=request.form['age']


    db = Db()
    try:
        image = request.files['pic']
        date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        image.save(r"C:\Users\HP\PycharmProjects\ADA\static\userpic\\" + date + '.jpg')
        path = "/static/userpic/" + date + '.jpg'

        if request.files!="":
            if image.filename!="":
                db.update("update client set client_name='" + name + "',phone_number='"+phone+"',gender='"+gender+"',age='"+age+"',image='"+str(path)+"',location='"+location+"',zip_code='"+zipcode+"',emergency_contact='"+emergency+"',email_id='"+email+"' WHERE client_id='"+str(lid)+"'")
                return jsonify(status="ok")
            else:
                db.update("update client set client_name='" + name + "',phone_number='" + phone + "',gender='" + gender + "',age='" + age + "',location='" + location + "',zip_code='" + zipcode + "',emergency_contact='" + emergency + "',email_id='" + email + "' WHERE client_id='" + str(lid) + "'")
                return jsonify(status="ok")
        else:
            db.update("update client set client_name='" + name + "',phone_number='" + phone + "',gender='" + gender + "',age='" + age + "',location='" + location + "',zip_code='" + zipcode + "',emergency_contact='" + emergency + "',email_id='" + email + "' WHERE client_id='" + str(lid) + "'")
            return jsonify(status="ok")
    except Exception as e:
        db.update(
            "update client set client_name='" + name + "',phone_number='" + phone + "',gender='" + gender + "',age='" + age + "',location='" + location + "',zip_code='" + zipcode + "',emergency_contact='" + emergency + "',email_id='" + email + "' WHERE client_id='" + str(
                lid) + "'")
        return jsonify(status="ok")
@app.route('/and_view_doctor',methods=['post'])
def and_view_doctor():
    db=Db()
    res=db.select("select * from doctor,login where doctor.doctor_id=login.login_id and login.user_type='doctor'")
    if len(res)>0:
        return jsonify(status="ok",data=res)
    else:
        return  jsonify(status="no")


@app.route('/and_view_hospital',methods=['post'])
def and_view_hospital():
    db=Db()
    res=db.select("select * from hospital,login where hospital.hospital_id=login.login_id and login.user_type='hospital'")
    if len(res)>0:
        return jsonify(status="ok",data=res)
    else:
        return  jsonify(status="no")




@app.route('/and_search_doctor',methods=['post'])
def and_search_doctor():
    dn=request.form['doctorname']
    print(dn)

    db=Db()
    res=db.select("select * from doctor,login where doctor.doctor_id=login.login_id and login.user_type='doctor' and doctor.specialization LIKE '%"+dn+"%'")
    if len(res)>0:
        return jsonify(status="ok",data=res)
    else:
        return  jsonify(status="no")


@app.route('/and_search_hospital',methods=['post'])
def and_search_hospital():
    hn=request.form['hospitalname']
    db=Db()
    res=db.select("select * from hospital,login where hospital.hospital_id=login.login_id and login.user_type='hospital' and hospital.hospital_name LIKE '%"+hn+"%' ")
    if len(res)>0:
        return jsonify(status="ok",data=res)
    else:
        return  jsonify(status="no")


@app.route('/and_full_doctor', methods=['post'])
def and_full_doctor():
    did = request.form['did']


    db = Db()
    res = db.selectOne("select * from doctor where doctor.doctor_id='"+did+"'")
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")


@app.route('/and_full_hospital', methods=['post'])
def and_full_hospital():
    hid = request.form['hid']
    db = Db()
    res = db.selectOne( "select * from hospital where hospital.hospital_id='"+hid+"' ")
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")



@app.route('/and_view_schedule', methods=['post'])
def and_view_schedule():
    did = request.form['dd']
    print(did)

    db = Db()
    res = db.select("select * from schedule where doctor_id='"+did+"'")
    # print(res)
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")

@app.route('/and_booking', methods=['post'])
def and_booking():
    sid = request.form['sid']
    lid = request.form['id']
    print(sid)

    db = Db()
    qry=db.selectOne("select * from booking where schedule_id='"+sid+"' and client_id='"+lid+"'")
    if qry is not None:
        return jsonify(status="already")
    else:
        db.insert("insert into booking value ('','"+sid+"',curdate(),curtime(),'pending','"+lid+"')")
        return jsonify(status="ok")

@app.route('/and_view_appointment_history', methods=['post'])
def and_view_appointment_history():
    lid = request.form['id']


    db = Db()
    res = db.select("select * from schedule,doctor,booking where booking.schedule_id=schedule.schedule_id and schedule.doctor_id=doctor.doctor_id and booking.client_id='"+lid+"'")
    # print(res)
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")

@app.route('/and_cancel_appointment', methods=['post'])
def and_cancel_appointment():
    bid = request.form['bid']

    db = Db()
    db.delete("delete from booking where booking_id='"+bid+"'")
    return jsonify(status="ok")

@app.route('/and_view_prescription', methods=['post'])
def and_view_prescription():
    bid = request.form['bid']
    db = Db()
    res = db.select("select * from prescription,medicine where prescription.medicine_id=medicine.medicine_id and prescription.booking_id='"+bid+"'")
    # print(res)
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")

@app.route('/and_view_test_result', methods=['post'])
def and_view_test_result():
    bid = request.form['bid']
    db = Db()
    res = db.select("select * from test,lab_test where lab_test.test_id=test.test_id and lab_test.booking_id='"+bid+"'")
    # print(res)
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")



@app.route("/and_registration",methods=['post'])
def and_registration():
    client_name=request.form['name']
    phone_number= request.form['phone']
    gender = request.form['gender']
    age = request.form['age']
    location = request.form['location']
    zip_code = request.form['zip_code']
    emergency_number = request.form['emergency']
    email_id = request.form['email']
    password = request.form['password']
    repassword = request.form['repassword']
    pic = request.files['pic']
    date=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    pic.save(r"C:\Users\HP\PycharmProjects\ADA\static\userpic\\"+date+'.jpg')
    path="/static/userpic/"+date+'.jpg'
    if password==repassword:
        db=Db()
        res=db.insert("insert into login values ('','"+email_id+"','"+password+"','client')")
        db.insert("insert into client values ('"+str(res)+"','"+client_name+"','"+phone_number+"','"+gender+"','"+age+"','"+path+"','"+location+"','"+zip_code+"','"+emergency_number+"','"+email_id+"')")
        return jsonify(status="ok")
    else:
        return jsonify(status="mismatch")

@app.route('/and_search_lab',methods=['post'])
def and_search_lab():
    # ln=request.form['labname']
    # print(ln)

    db=Db()
    res=db.select("select * from lab,login where lab.lab_id=login.login_id and login.user_type='lab'")
    if len(res)>0:
        return jsonify(status="ok",data=res)
    else:
        return  jsonify(status="no")



@app.route('/and_search_lab2',methods=['post'])
def and_search_lab2():
    ln=request.form['labname']
    print(ln)

    db=Db()
    res=db.select("select * from lab,login where lab.lab_id=login.login_id and login.user_type='lab' and lab.location LIKE '%"+ln+"%'")
    if len(res)>0:
        return jsonify(status="ok",data=res)
    else:
        return  jsonify(status="no")


@app.route('/and_view_today_appointment', methods=['post'])
def and_view_today_appointment():
    aid = request.form['id']


    db = Db()
    res = db.select("select * from booking,schedule,doctor where booking.schedule_id=schedule.schedule_id and schedule.doctor_id=doctor.doctor_id and booking.client_id='"+aid+"' and schedule.date=curdate() and booking.status='booked'")
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")


@app.route('/bmi_calculator',methods=['post'])
def bmi_calculator():
    height=request.form['h']
    weight=request.form['w']
    hh=int(height)/100
    h=hh*hh
    result=int(weight)/(h)
    # rslt=int(result)
    rslt=round(result,0)
    # print(r)
    if rslt < 18.5:
        return jsonify(status="ok",data="Underweight")
    if rslt < 25:
        return jsonify(status="ok",data="Healthy")
    if rslt < 30:
        return  jsonify(status="ok",data="Overweight")
    else:
        return jsonify(status="ok",data="Obesity")



@app.route('/and_view_result',methods=['post'])
def and_view_result():
    lid = request.form['id']

    db = Db()
    res = db.select("select * from lab_result,lab where lab_result.lab_id=lab.lab_id and lab_result.client_id='" + lid + "'")
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")



@app.route('/and_add_record',methods=['post'])
def and_add_record():
    uid = request.form['lid']
    vdyo=request.form['vid']
    extn=request.form['vid_type']
    date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    a=base64.b64decode(vdyo)
    f=open(r"C:\Users\HP\PycharmProjects\ADA\static\record\\"+date+ "."+extn,"wb")
    record="/static/record/"+date+"."+extn
    f.write(a)
    f.close()
    db=Db()
    db.insert("insert into client_data_record VALUES ('','"+uid+"',curdate(),'"+str(record)+"')")
    return jsonify(status="ok")


# @app.route('/and_add_work',methods=['post'])
# def and_add_work():
#     work=request.form['wrk']
#     des=request.form['det']
#     uid = request.form['lid']
#     vdyo=request.form['vid']
#     extn=request.form['vid_type']
#     date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
#     a=base64.b64decode(vdyo)
#     f=open(r"D:\Project\sngcas\backup\smart_career\static\pic\\"+date+ ".mp4","wb")
#     ss="/static/pic/"+date+".mp4"
#     f.write(a)
#     f.close()
#     db=Db()
#     db.insert("insert into work VALUES ('','"+uid+"',curdate(),'"+work+"','"+des+"','"+str(ss)+"')")
#     return jsonify(status="ok")



@app.route('/and_view_records',methods=['post'])
def and_view_records():
    uid=request.form['dd']
    db=Db()
    res=db.select("select * from client_data_record where client_id='"+uid+"'")
    return jsonify(status="ok",data=res)


@app.route('/and_delete_record', methods=['post'])
def and_delete_record():
    rid=request.form['sid']
    db = Db()
    res=db.delete("delete from client_data_record where record_id='"+rid+"'")
    return jsonify(status="ok")

@app.route('/and_view_send_records',methods=['post'])
def and_view_send_record():
    uid = request.form['id']
    print(uid)
    db = Db()
    res = db.select("select * from client_data_record where client_id='" + uid + "'")
    print(res)
    return jsonify(status="ok", data=res)


@app.route('/and_share_record', methods=['post'])
def and_share_record():
    bid = request.form['bid']
    rid = request.form['rid']
    # print(sid)

    db = Db()
    qry=db.selectOne("select * from share where booking_id='"+bid+"' and record_id='"+rid+"'")
    if qry is not None:
        return jsonify(status="already")
    else:
        db.insert("insert into share value ('','"+bid+"','"+rid+"')")
        return jsonify(status="ok")


if __name__ == '__main__':
              # app.run(debug=True, port=1234,host="0.0.0.0")
                  app.run(debug=True, port=4000)
