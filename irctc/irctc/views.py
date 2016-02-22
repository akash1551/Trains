from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import json
from django.db import IntegrityError
from datetime import timedelta
import time
import re
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import calendar
from django.db import transaction
from irctc.models import UserDetail,Reservation,Train,Station,Location

def validate_mobile(value):
    rule = re.compile(r'^(\+91[\-\s]?)?[0]?[1789]\d{9}$')
    if not rule.search(value):
        return False
    else:
        return value

@transaction.atomic
def register_new_user(request):
	json_obj=json.loads(request.body)
    json_obj=json_obj['userInfo']

    if User.objects.filter(username = json_obj['userName']).exists():
        return HttpResponse(json.dumps({"validation":"Username is already exist.","status":False}), content_type="application/json")
    username = json_obj['userName']
    firstName = json_obj['firstName']
    lastName = json_obj['lastName']
    password = json_obj['password']
    password1 = json_obj['confirmPassword']
    if password != password1:
        return HttpResponse(json.dumps({"validation":"Passwords are not Matched","status":False}), content_type="application/json")
    if User.objects.filter(email = json_obj['email']).exists():
        return HttpResponse(json.dumps({"validation":"Email is already exist.Try with another Email.","status":False}), content_type="application/json")
    email = json_obj['email']
    if json_obj['address'] is None:
        return HttpResponse(json.dumps({"validation":"Please Enter Your Address...!","status":False}), content_type="application/json")
    else:
        address = json_obj['address']

    mobileNo = json_obj['mobileNo']
    mobileNo = int(mobileNo)
    mobileNo = validate_mobile(str(mobileNo))
    if mobileNo == False:
        return HttpResponse(json.dumps([{"validation": "This mobile number is already used..please try with another one.", "status": False}]), content_type = "application/json")
    else:
        mobileNo = json_obj['mobileNo']
        user_obj = User(first_name=firstName,last_name=lastName,username=username,email=email,password=password)
        user_obj.set_password(password)
        user_obj.save()
        userdetail_obj = UserDetail(user=user_obj,address=address,mobileNo=mobileNo)
        userdetail_obj.save()
        return HttpResponse(json.dumps({"validation":"Registration Successful.","redirecturl":"#/login","status":True}), content_type="application/json")

def user_login(request):
    data_dict = json.loads(request.body)
    username = data_dict['username']
    password = data_dict['password']
    user = auth.authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            auth.login(request,user)
            return HttpResponse(json.dumps({"validation":"Login Successful","status":True,'redirecturl':"/userHome"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"validation":"Invalid Login","status":False}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"validation":"Invalid Login Credentials","status":False}), content_type="application/json")

@transaction_atomic
def reservation(request):
	if request.user.is_authenticated():
		jsonObj = json.loads(request.body)
		trainNo = jsonObj['trainNo']
		trainName = jsonObj['trainName']
		journeyDate = jsonObj['journeyDate']
        className = jsonObj['className']
        source = jsonObj['source']
        destination = jsonObj['destination']
        firstName = jsonObj['firstName']
        lastName = jsonObj['lastName']
        gender = jsonObj['gender']
        age = jsonObj['age']
        address = jsonObj['address']
        pnrNo = generate_prn_number(trainNo)
        reservationObj = Reservation(pnrNo=pnrNo,trainNo=trainNo,trainName=trainName,journeyDate=journeyDate,
            className=className,source=source,destination=destination,firstName=firstName,
            lastName=lastName,gender=gender,age=age,address=address)
        reservationObj.save()
        return HttpResponse(json.dumps({"validation":"Your reservation process is completed Successfully.","status":True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"validation":"You are not logged in.Please login first.","status":False}), content_type="application/json")

def generate_prn_number(qry):
    if request.user.is_authenticated():
        currentDate = datetime.datetime.today().strftime('%d%m%Y')
        pnrNo = '10'+str(currentDate)+'{0:0{width}}'.format(qry.id, width=8)
        return pnrNo

